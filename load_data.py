import duckdb
import os

DB_FILE = 'ecommerce.duckdb'
DATA_DIR = 'archive'

print(f"Connecting to DuckDB database: {DB_FILE}...")
con = duckdb.connect(DB_FILE)

# 1. Create Schema
con.execute("CREATE SCHEMA IF NOT EXISTS amazon_brazil;")

# 2. Ingest Tables from CSV files
tables = {
    "customers": f"""
        CREATE OR REPLACE TABLE amazon_brazil.customers AS 
        SELECT 
            customer_id, 
            customer_unique_id, 
            customer_zip_code_prefix 
        FROM read_csv_auto('{DATA_DIR}/olist_customers_dataset.csv');
    """,
    "orders": f"""
        CREATE OR REPLACE TABLE amazon_brazil.orders AS 
        SELECT 
            order_id, 
            customer_id, 
            order_status, 
            order_purchase_timestamp::TIMESTAMP as order_purchase_timestamp,
            order_approved_at::TIMESTAMP as order_approved_at,
            order_delivered_carrier_date::TIMESTAMP as order_delivered_carrier_date,
            order_delivered_customer_date::TIMESTAMP as order_delivered_customer_date,
            order_estimated_delivery_date::TIMESTAMP as order_estimated_delivery_date
        FROM read_csv_auto('{DATA_DIR}/olist_orders_dataset.csv');
    """,
    "payments": f"""
        CREATE OR REPLACE TABLE amazon_brazil.payments AS 
        SELECT 
            order_id, 
            payment_sequential, 
            payment_type, 
            payment_installments, 
            payment_value 
        FROM read_csv_auto('{DATA_DIR}/olist_order_payments_dataset.csv');
    """,
    "sellers": f"""
        CREATE OR REPLACE TABLE amazon_brazil.sellers AS 
        SELECT 
            seller_id, 
            seller_zip_code_prefix 
        FROM read_csv_auto('{DATA_DIR}/olist_sellers_dataset.csv');
    """,
    "products": f"""
        CREATE OR REPLACE TABLE amazon_brazil.products AS 
        SELECT 
            product_id, 
            product_category_name, 
            product_name_lenght as product_name_length, 
            product_description_lenght as product_description_length, 
            product_photos_qty, 
            product_weight_g, 
            product_length_cm, 
            product_height_cm, 
            product_width_cm 
        FROM read_csv_auto('{DATA_DIR}/olist_products_dataset.csv');
    """,
    "order_items": f"""
        CREATE OR REPLACE TABLE amazon_brazil.order_items AS 
        SELECT 
            order_id, 
            order_item_id, 
            product_id, 
            seller_id, 
            shipping_limit_date::TIMESTAMP as shipping_limit_date, 
            price, 
            freight_value 
        FROM read_csv_auto('{DATA_DIR}/olist_order_items_dataset.csv');
    """
}

for table_name, query in tables.items():
    print(f"Loading {table_name}...")
    con.execute(query)

print("\n--- Data Ingestion Complete! ---")
for tbl in tables.keys():
    cnt = con.execute(f"SELECT count(*) FROM amazon_brazil.{tbl}").fetchone()[0]
    print(f"  amazon_brazil.{tbl:<12}: {cnt:>10,d} rows")

con.close()
