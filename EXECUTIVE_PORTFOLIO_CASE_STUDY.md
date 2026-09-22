# Executive Case Study: E-Commerce Marketplace Performance & Retention Strategy
**Role / Scope:** Business Analyst Portfolio Case Study  
**Multi-Tool Toolkit:** SQL (PostgreSQL / DuckDB), DBeaver GUI, Power BI (Star Schema & DAX), Python (Pandas, Seaborn, Jupyter)  
**Dataset:** 100,000+ Orders (~R$ 13.59M GMV) | Olist / Amazon Brazil Marketplace  

---

## 1. Executive Summary & Problem Statement
A major Brazilian e-commerce marketplace integrator experienced rapid top-line growth (scaling from R$ 120k/month in early 2017 to over R$ 1.0M/month in 2018). However, leadership needed visibility into **underlying customer churn, payment friction, and product category concentration** to sustain profitability.

**Core Objectives:**
1. Assess macro revenue trajectory and seasonal demand cycles.
2. Evaluate payment channel economics and risk.
3. Diagnose the customer lifecycle funnel (Repeat vs One-Time purchasing).
4. Deliver actionable recommendations for the executive leadership team.

---

## 2. Key Findings & Quantitative Insights

```
+------------------------------------------------------------------------------------+
|  Total GMV: R$ 13.59M  |  Total Orders: 99,441  |  AOV: R$ 136.70  |  Repeat Rate: 3.1%  |
+------------------------------------------------------------------------------------+
```

###  Finding 1: The "Leaky Bucket" Retention Crisis (Top Finding)
- **96.9% of customers are one-time purchasers** (93,099 out of 96,096 unique customers).
- Only **3.1%** of customers ever return for a second order, and only **19 customers** placed $\ge$ 5 orders.
- *Diagnosis:* High reliance on Customer Acquisition Cost (CAC) without post-purchase lifecycle retention.

###  Finding 2: Payment Economics & Boleto Latency
- **Credit Card** dominates transaction volume (**73.9%**) and drives the highest ticket size (**R$ 163.30 AOV**), heavily driven by installment options.
- **Boleto (Cash voucher)** represents **19.0%** of orders (**R$ 145.10 AOV**). While essential for reaching unbanked consumers, Boleto creates a 1–3 day settlement latency and higher abandonment rates.

###  Finding 3: 80/20 Pareto Concentration in Product Categories
- Top 5 categories (*Beleza & Saúde, Relógios Presentes, Cama Mesa & Banho, Esporte Lazer, Informática*) generate over **35% of total gross merchandise value**.
- High price dispersion (> R$ 500 spread) exists in electronics and fashion, indicating an opportunity for tiered product positioning.

###  Finding 4: Seasonality & Demand Spikes
- **Q4 Surge:** November records massive spikes in GMV (+56% MoM) driven by Black Friday campaigns.
- Revenue stabilizes between **R$ 950k – R$ 1.05M** per month during standard operating quarters.

---

## 3. Strategic Business Recommendations (Action Plan)

| Pillar | Strategic Recommendation | Expected Business Impact |
| :--- | :--- | :--- |
| **Customer Retention** | Launch automated post-delivery email triggers (replenishment coupons 30 days post-delivery) and a subscription tier for consumables (*Health & Beauty*). | Boost repeat customer rate from **3.1% to 6.5%**, reducing blended CAC. |
| **Payment Optimization** | Introduce **Pix** (instant central bank rails) to replace legacy Boleto vouchers. | Reduce order settlement latency to instant and decrease cart abandonment by **8–12%**. |
| **Supply Chain & Sellers** | Implement targeted fulfillment partnerships for top 5 category sellers ahead of September. | Ensure sub-3-day delivery and avoid stockouts during the November Black Friday peak. |
| **Catalog Quality** | Enforce automated taxonomy validation to remove orphaned/single-character product categories. | Improve search accuracy and catalog conversion rate. |

---

## 4. Multi-Tool Technical Architecture

This project demonstrates an end-to-end analytics workflow across multiple database and visualization tools:

```
[Raw CSVs: archive/] 
   └──> [ETL: load_data.py] 
           └──> [Database Layer: DuckDB (ecommerce.duckdb) + DBeaver GUI + SQL Script]
                   ├──> [Data Exploration: Amazon_Business_Case_Study.ipynb (Jupyter + Seaborn)]
                   └──> [BI Modeling: export_powerbi_data.py -> powerbi_data/ -> Power BI / Tableau]
```

---

## 5. Repository File Guide & Functional Breakdown

A comprehensive index explaining the exact function and business value of every file in this repository:

| File / Folder | Category | Purpose & Functional Description |
| :--- | :--- | :--- |
| **`EXECUTIVE_PORTFOLIO_CASE_STUDY.md`** | **Executive Brief** | High-level 1-page business case study written in Amazon-style memo format for hiring managers and leadership. |
| **`README.md`** | **Documentation** | Master repository guide covering architecture, skills matrix, key findings, and step-by-step local setup instructions. |
| **`amazon_business_analysis.sql`** | **SQL Engine** | Production-ready SQL script containing **19 analytical queries** across 3 tiers (Data Quality Audits, Customer Segmentation, and Window Functions like `LAG`, `RANK`, and `SUM() OVER`). |
| **`load_data.py`** | **Data Engineering / ETL** | Automated Python pipeline that reads raw CSVs, enforces data types, cleans date formats, and creates the structured `amazon_brazil` schema in DuckDB in < 2 seconds. |
| **`ecommerce.duckdb`** | **Database** | Embedded, serverless columnar SQL database file allowing zero-configuration local querying via Python, CLI, or **DBeaver Community GUI**. |
| **`interactive_sql.py`** | **Developer Tooling** | Live interactive command-line interface (CLI) to execute ad-hoc SQL queries against `ecommerce.duckdb` with formatted ASCII table output. |
| **`run_analysis.py`** | **Automation & QA** | Automated test script that validates and executes core SQL business queries against the database programmatically to guarantee zero runtime errors. |
| **`Amazon_Business_Case_Study.ipynb`** | **EDA & Storytelling** | Master Jupyter Notebook marrying DuckDB SQL extraction, Pandas data processing, Seaborn statistical visualization, and narrative business diagnostics. |
| **`Amazon_Business_Case_Study.html`** | **Web Deliverable** | Fully rendered HTML export of the notebook allowing recruiters/managers to review all code, charts, and analysis in any browser without installing Python. |
| **`build_notebook.py`** | **Notebook Generator** | Python utility script used to programmatically generate and format the structured Jupyter notebook cells and markdown blocks. |
| **`export_powerbi_data.py`** | **Dimensional Modeling** | Data transformation pipeline that converts relational SQL tables into an optimized **Star-Schema** with Fact and Dimension CSVs. |
| **`powerbi_data/`** | **BI Datasets** | Directory of clean dimensional modeling tables ready for Power BI / Tableau import: `fact_orders.csv`, `fact_order_items.csv`, `fact_payments.csv`, `dim_customers.csv`, `dim_products.csv`, `dim_sellers.csv`, and `kpi_monthly_summary.csv`. |
| **`POWERBI_TABLEAU_GUIDE.md`** | **BI Blueprint** | Complete enterprise BI implementation guide containing 1-to-many relationship mappings, DAX measure formulas (`GMV`, `AOV`, `Repeat Rate`, `MoM Growth`), and multi-page dashboard wireframes. |
| **`Amazon_SQL_Analysis_Report.pdf`** | **Formal Report** | Publication-grade PDF report summarizing SQL methodologies, schema structures, and analytical conclusions. |
| **`Jupyter_Notebook_Amazon_Business_Case_Study.pdf`** | **Visual Deliverable** | Print-ready PDF version of the complete data science and exploratory analysis notebook. |
| **`archive/`** | **Raw Data** | Source directory containing raw CSV datasets (100,000+ e-commerce transactions across customers, orders, payments, products, and sellers). |
