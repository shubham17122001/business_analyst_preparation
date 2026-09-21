import os
import duckdb
import pandas as pd

OUTPUT_DIR = 'powerbi_data'
os.makedirs(OUTPUT_DIR, exist_ok=True)

con = duckdb.connect('ecommerce.duckdb')

print("="*60)
print(f" Exporting Clean Star-Schema Data for Power BI / Tableau")
print("="*60)

# 1. Fact Tables
print("Exporting Fact: Orders...")
con.execute("""
    SELECT 
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_customer_date,
        order_estimated_delivery_date
    FROM amazon_brazil.orders;
""").df().to_csv(f"{OUTPUT_DIR}/fact_orders.csv", index=False)

print("Exporting Fact: Order Items...")
con.execute("""
    SELECT 
        order_id,
        order_item_id,
        product_id,
        seller_id,
        price,
        freight_value,
        (price + freight_value) AS total_item_value
    FROM amazon_brazil.order_items;
""").df().to_csv(f"{OUTPUT_DIR}/fact_order_items.csv", index=False)

print("Exporting Fact: Payments...")
con.execute("""
    SELECT 
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value
    FROM amazon_brazil.payments;
""").df().to_csv(f"{OUTPUT_DIR}/fact_payments.csv", index=False)

# 2. Dimension Tables
print("Exporting Dimension: Customers...")
con.execute("""
    SELECT 
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix
    FROM amazon_brazil.customers;
""").df().to_csv(f"{OUTPUT_DIR}/dim_customers.csv", index=False)

print("Exporting Dimension: Products...")
con.execute("""
    SELECT 
        product_id,
        COALESCE(product_category_name, 'Uncategorized') AS product_category_name,
        product_name_length,
        product_photos_qty,
        product_weight_g
    FROM amazon_brazil.products;
""").df().to_csv(f"{OUTPUT_DIR}/dim_products.csv", index=False)

print("Exporting Dimension: Sellers...")
con.execute("""
    SELECT 
        seller_id,
        seller_zip_code_prefix
    FROM amazon_brazil.sellers;
""").df().to_csv(f"{OUTPUT_DIR}/dim_sellers.csv", index=False)

# 3. Curated Business Summary Table (Monthly KPIs)
print("Exporting Analytical KPI Summary: Monthly Metrics...")
con.execute("""
    WITH monthly_orders AS (
        SELECT 
            DATE_TRUNC('month', o.order_purchase_timestamp) AS sale_month,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COUNT(DISTINCT o.customer_id) AS unique_customers,
            ROUND(SUM(oi.price), 2) AS total_gmv,
            ROUND(AVG(oi.price), 2) AS avg_item_price
        FROM amazon_brazil.orders o
        JOIN amazon_brazil.order_items oi
            ON o.order_id = oi.order_id
        GROUP BY sale_month
    )
    SELECT 
        sale_month,
        total_orders,
        unique_customers,
        total_gmv,
        avg_item_price,
        ROUND((total_gmv - LAG(total_gmv) OVER (ORDER BY sale_month)) * 100.0 / LAG(total_gmv) OVER (ORDER BY sale_month), 2) AS mom_gmv_growth_pct
    FROM monthly_orders
    ORDER BY sale_month;
""").df().to_csv(f"{OUTPUT_DIR}/kpi_monthly_summary.csv", index=False)

print("\n--- Export Finished! ---")
print(f"All files saved in: '{OUTPUT_DIR}/'")
con.close()
