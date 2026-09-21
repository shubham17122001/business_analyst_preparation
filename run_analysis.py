import duckdb
import pandas as pd

# Set pandas display options for clean terminal output
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

con = duckdb.connect('ecommerce.duckdb')

def run_query(title, sql):
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)
    df = con.execute(sql).df()
    print(df.head(10))
    if len(df) > 10:
        print(f"... ({len(df)} total rows returned)")
    return df

# Let's test a few sample queries from the project:

# Part 1 - Q1: Average payment value per payment type
run_query(
    "Part I - Q1: Average Payment Value by Payment Type",
    """
    SELECT 
        payment_type,
        ROUND(AVG(payment_value)) AS rounded_avg_payment
    FROM amazon_brazil.payments
    GROUP BY payment_type
    ORDER BY rounded_avg_payment ASC;
    """
)

# Part 1 - Q2: Percentage of total orders per payment type
run_query(
    "Part I - Q2: Percentage of Total Orders by Payment Type",
    """
    SELECT 
        payment_type, 
        ROUND(COUNT(order_id) * 100.0 / SUM(COUNT(order_id)) OVER (), 1) AS percentage_orders
    FROM amazon_brazil.payments
    GROUP BY payment_type
    ORDER BY percentage_orders DESC;
    """
)

# Part 2 - Q4: Customer Segmentation (New, Returning, Loyal)
run_query(
    "Part II - Q4: Customer Segmentation",
    """
    WITH customer_orders AS (
        SELECT 
            c.customer_unique_id,
            COUNT(o.order_id) AS total_orders
        FROM amazon_brazil.orders o
        JOIN amazon_brazil.customers c
            ON o.customer_id = c.customer_id
        GROUP BY c.customer_unique_id
    )
    SELECT 
        CASE 
            WHEN total_orders = 1 THEN 'New'
            WHEN total_orders BETWEEN 2 AND 4 THEN 'Returning'
            ELSE 'Loyal'
        END AS customer_type,
        COUNT(*) AS customer_count
    FROM customer_orders
    GROUP BY customer_type
    ORDER BY customer_count DESC;
    """
)

# Part 3 - Q7: MoM Growth for Payment Types in 2018
run_query(
    "Part III - Q7: Month-over-Month Growth by Payment Type (2018)",
    """
    WITH monthly_sales AS (
        SELECT 
            p.payment_type,
            DATE_TRUNC('month', o.order_purchase_timestamp) AS sale_month,
            SUM(oi.price) AS monthly_total
        FROM amazon_brazil.orders o
        JOIN amazon_brazil.order_items oi
            ON o.order_id = oi.order_id
        JOIN amazon_brazil.payments p
            ON o.order_id = p.order_id
        WHERE EXTRACT(YEAR FROM o.order_purchase_timestamp) = 2018
        GROUP BY p.payment_type, sale_month
    )
    SELECT 
        payment_type,
        sale_month,
        ROUND(monthly_total, 2) AS monthly_total,
        ROUND(
            (monthly_total - LAG(monthly_total) OVER (
                PARTITION BY payment_type 
                ORDER BY sale_month
            )) 
            * 100.0 
            / LAG(monthly_total) OVER (
                PARTITION BY payment_type 
                ORDER BY sale_month
            ),
            2
        ) AS monthly_growth_pct
    FROM monthly_sales
    ORDER BY payment_type, sale_month;
    """
)

con.close()
