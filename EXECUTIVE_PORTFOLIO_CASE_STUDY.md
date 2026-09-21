# 🛒 Executive Case Study: E-Commerce Marketplace Performance & Retention Strategy
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

### 🚨 Finding 1: The "Leaky Bucket" Retention Crisis (Top Finding)
- **96.9% of customers are one-time purchasers** (93,099 out of 96,096 unique customers).
- Only **3.1%** of customers ever return for a second order, and only **19 customers** placed $\ge$ 5 orders.
- *Diagnosis:* High reliance on Customer Acquisition Cost (CAC) without post-purchase lifecycle retention.

### 💳 Finding 2: Payment Economics & Boleto Latency
- **Credit Card** dominates transaction volume (**73.9%**) and drives the highest ticket size (**R$ 163.30 AOV**), heavily driven by installment options.
- **Boleto (Cash voucher)** represents **19.0%** of orders (**R$ 145.10 AOV**). While essential for reaching unbanked consumers, Boleto creates a 1–3 day settlement latency and higher abandonment rates.

### 🛍️ Finding 3: 80/20 Pareto Concentration in Product Categories
- Top 5 categories (*Beleza & Saúde, Relógios Presentes, Cama Mesa & Banho, Esporte Lazer, Informática*) generate over **35% of total gross merchandise value**.
- High price dispersion (> R$ 500 spread) exists in electronics and fashion, indicating an opportunity for tiered product positioning.

### 📈 Finding 4: Seasonality & Demand Spikes
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

## 4. Multi-Tool Technical Architecture & Skillset Matrix

This project demonstrates an end-to-end analytics workflow across multiple database and visualization tools:

```
[Raw CSVs: archive/] 
   └──> [ETL: load_data.py] 
           └──> [Database Layer: DuckDB (ecommerce.duckdb) + DBeaver GUI + SQL Script]
                   ├──> [Data Exploration: Amazon_Business_Case_Study.ipynb (Jupyter + Seaborn)]
                   └──> [BI Modeling: export_powerbi_data.py -> powerbi_data/ -> Power BI / Tableau]
```

### Component Breakdown:
- **`archive/`**: Raw dataset containing 100k+ transactions from Kaggle.
- **`ecommerce.duckdb` & `amazon_business_analysis.sql`**: Embedded SQL analytical engine queried through **DBeaver Community GUI** and custom Python runners (`interactive_sql.py`, `run_analysis.py`).
- **`Amazon_Business_Case_Study.ipynb`**: Complete Jupyter Notebook showcasing Python data analysis, SQL-in-Python, and publication-ready Seaborn/Matplotlib visual dashboards.
- **`powerbi_data/` & `POWERBI_TABLEAU_GUIDE.md`**: Curated Star-Schema dimensional model (`dim_customers`, `dim_products`, `dim_sellers`, `fact_orders`, `fact_order_items`, `fact_payments`) with custom DAX measures (`Total GMV`, `AOV`, `Repeat Rate`, `MoM Growth`).
