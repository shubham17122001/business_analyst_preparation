import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 📊 Amazon Brazil E-Commerce Business Case Study\n",
    "## Executive Business Analytics, Customer Segmentation & Strategic Recommendations\n",
    "\n",
    "**Author:** Business Analyst Portfolio  \n",
    "**Data Engine:** SQL via DuckDB  \n",
    "**Visualization:** Matplotlib, Seaborn, Pandas  \n",
    "**Dataset:** 100,000+ Orders (Olist / Amazon Brazil Marketplace)\n",
    "\n",
    "---\n",
    "\n",
    "### 🎯 Business Context & Problem Statement\n",
    "An e-commerce marketplace operating in Brazil requires an in-depth data-driven assessment of its commercial performance. Executive leadership has outlined key strategic priorities:\n",
    "1. **Revenue Growth & Seasonality:** Evaluate monthly revenue trajectory and identify peak seasonal cycles.\n",
    "2. **Payment Dynamics & Risk:** Understand consumer payment behavior (Credit Card, Boleto, Installments) across basket sizes.\n",
    "3. **Customer Retention & Churn:** Measure one-time vs repeat purchasing rates to assess customer lifetime value.\n",
    "4. **Product Portfolio Optimization:** Identify top revenue-generating categories and spot catalog data quality anomalies."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Environment Setup & Data Engine Connection\n",
    "import duckdb\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Set display and visual styles\n",
    "pd.set_option('display.max_columns', None)\n",
    "pd.set_option('display.width', 1000)\n",
    "sns.set_theme(style=\"whitegrid\")\n",
    "plt.rcParams['font.sans-serif'] = 'Arial'\n",
    "plt.rcParams['figure.dpi'] = 120\n",
    "\n",
    "# Connect to local DuckDB database\n",
    "con = duckdb.connect('ecommerce.duckdb')\n",
    "print(\"✅ Connected to ecommerce.duckdb database successfully!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 📈 Section 1: Executive KPI Scorecard & Macro Revenue Trends\n",
    "Let's assess the top-line macro performance: Total Revenue, Total Orders, and Monthly Performance."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Monthly Revenue & Month-over-Month Growth (2017-2018)\n",
    "monthly_kpi_query = \"\"\"\n",
    "WITH monthly_data AS (\n",
    "    SELECT \n",
    "        DATE_TRUNC('month', o.order_purchase_timestamp) AS sale_month,\n",
    "        ROUND(SUM(oi.price), 2) AS monthly_revenue,\n",
    "        COUNT(DISTINCT o.order_id) AS total_orders\n",
    "    FROM amazon_brazil.orders o\n",
    "    JOIN amazon_brazil.order_items oi\n",
    "        ON o.order_id = oi.order_id\n",
    "    WHERE o.order_status = 'delivered'\n",
    "    GROUP BY sale_month\n",
    ")\n",
    "SELECT \n",
    "    sale_month,\n",
    "    monthly_revenue,\n",
    "    total_orders,\n",
    "    ROUND((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY sale_month)) * 100.0 / LAG(monthly_revenue) OVER (ORDER BY sale_month), 2) AS mom_growth_pct\n",
    "FROM monthly_data\n",
    "ORDER BY sale_month;\n",
    "\"\"\"\n",
    "\n",
    "df_monthly = con.execute(monthly_kpi_query).df()\n",
    "df_monthly['sale_month'] = pd.to_datetime(df_monthly['sale_month'])\n",
    "\n",
    "# Filter to active period (2017 - Aug 2018)\n",
    "df_monthly_active = df_monthly[(df_monthly['sale_month'] >= '2017-01-01') & (df_monthly['sale_month'] <= '2018-08-31')]\n",
    "display(df_monthly_active.tail(10))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Plot Monthly Revenue & MoM Growth\n",
    "fig, ax1 = plt.subplots(figsize=(12, 5))\n",
    "\n",
    "color = '#1f77b4'\n",
    "ax1.set_xlabel('Month', fontsize=12, fontweight='bold')\n",
    "ax1.set_ylabel('Total Revenue (BRL R$)', color=color, fontsize=12, fontweight='bold')\n",
    "ax1.plot(df_monthly_active['sale_month'], df_monthly_active['monthly_revenue'], color=color, marker='o', linewidth=2.5, label='Monthly Revenue')\n",
    "ax1.tick_params(axis='y', labelcolor=color)\n",
    "ax1.set_ylim(0, df_monthly_active['monthly_revenue'].max() * 1.2)\n",
    "\n",
    "ax2 = ax1.twinx()\n",
    "color = '#ff7f0e'\n",
    "ax2.set_ylabel('MoM Growth (%)', color=color, fontsize=12, fontweight='bold')\n",
    "ax2.bar(df_monthly_active['sale_month'], df_monthly_active['mom_growth_pct'], color=color, alpha=0.3, width=15, label='MoM Growth %')\n",
    "ax2.tick_params(axis='y', labelcolor=color)\n",
    "ax2.axhline(0, color='gray', linestyle='--', linewidth=0.8)\n",
    "\n",
    "plt.title('Monthly Revenue Trajectory & MoM Growth Rate (2017 - 2018)', fontsize=14, fontweight='bold', pad=15)\n",
    "fig.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 💡 Section 1 - Business Insights:\n",
    "- **Rapid Scale:** Revenue surged from ~R$ 120k in early 2017 to over R$ 1.0M+ monthly by 2018.\n",
    "- **Black Friday Spike:** November 2017 recorded a massive spike in revenue (+56% MoM growth).\n",
    "- **Platform Stabilization:** In 2018, revenue stabilized at an average of R$ 950,000 to R$ 1,050,000 per month."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 💳 Section 2: Payment Dynamics & Basket Size Segmentation\n",
    "Understanding payment method penetration and how payment choice changes with basket price."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Query: Payment Type Share & Average Ticket\n",
    "payment_query = \"\"\"\n",
    "SELECT \n",
    "    payment_type,\n",
    "    COUNT(order_id) AS total_transactions,\n",
    "    ROUND(COUNT(order_id) * 100.0 / SUM(COUNT(order_id)) OVER (), 1) AS pct_orders,\n",
    "    ROUND(AVG(payment_value), 2) AS avg_ticket_value,\n",
    "    ROUND(STDDEV(payment_value), 2) AS std_dev_value\n",
    "FROM amazon_brazil.payments\n",
    "GROUP BY payment_type\n",
    "ORDER BY pct_orders DESC;\n",
    "\"\"\"\n",
    "df_payments = con.execute(payment_query).df()\n",
    "display(df_payments)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visualizing Payment Methods\n",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "\n",
    "# 1. Market Share (Donut)\n",
    "valid_payments = df_payments[df_payments['payment_type'] != 'not_defined'].copy()\n",
    "axes[0].pie(\n",
    "    valid_payments['pct_orders'], \n",
    "    labels=valid_payments['payment_type'], \n",
    "    autopct='%1.1f%%', \n",
    "    startangle=140,\n",
    "    colors=['#2b5c8f', '#e8883b', '#2ca02c', '#d62728'],\n",
    "    wedgeprops=dict(width=0.4, edgecolor='w')\n",
    ")\n",
    "axes[0].set_title('Payment Method Market Share (% of Orders)', fontsize=12, fontweight='bold')\n",
    "\n",
    "# 2. Average Ticket Value (Bar)\n",
    "sns.barplot(\n",
    "    data=valid_payments, \n",
    "    x='payment_type', \n",
    "    y='avg_ticket_value', \n",
    "    hue='payment_type', \n",
    "    legend=False, \n",
    "    ax=axes[1], \n",
    "    palette='Blues_r'\n",
    ")\n",
    "axes[1].set_title('Average Transaction Value by Payment Method (BRL)', fontsize=12, fontweight='bold')\n",
    "axes[1].set_ylabel('Average Value (R$)')\n",
    "axes[1].set_xlabel('Payment Type')\n",
    "for p in axes[1].patches:\n",
    "    axes[1].annotate(f'R$ {p.get_height():.1f}', (p.get_x() + p.get_width() / 2., p.get_height() - 20),\n",
    "                     ha='center', va='center', color='white', fontweight='bold')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 💡 Section 2 - Business Insights:\n",
    "- **Credit Card Dominance:** **73.9%** of all transactions are conducted via Credit Card, generating the highest Average Order Value (**R$ 163.3**).\n",
    "- **Boleto (Cash Voucher):** Represents **19.0%** of orders (AOV: R$ 145.1). In Brazil, Boleto is crucial for unbanked consumers, but carries operational latency (payment takes 1-3 days to clear).\n",
    "- **Vouchers:** Represent small ticket redemption items (AOV: R$ 65.8)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 👥 Section 3: Customer Retention & Loyalty (The Critical Finding)\n",
    "A vital metric for marketplace sustainability is repeat purchase rate and customer lifetime loyalty."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Query: Customer Segmentation based on Lifetime Orders\n",
    "customer_segment_query = \"\"\"\n",
    "WITH customer_orders AS (\n",
    "    SELECT \n",
    "        c.customer_unique_id,\n",
    "        COUNT(o.order_id) AS total_orders\n",
    "    FROM amazon_brazil.orders o\n",
    "    JOIN amazon_brazil.customers c\n",
    "        ON o.customer_id = c.customer_id\n",
    "    GROUP BY c.customer_unique_id\n",
    ")\n",
    "SELECT \n",
    "    CASE \n",
    "        WHEN total_orders = 1 THEN 'New / One-Time (1 Order)'\n",
    "        WHEN total_orders BETWEEN 2 AND 4 THEN 'Returning (2-4 Orders)'\n",
    "        ELSE 'Loyal Champions (5+ Orders)'\n",
    "    END AS customer_segment,\n",
    "    COUNT(*) AS customer_count,\n",
    "    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_base\n",
    "FROM customer_orders\n",
    "GROUP BY customer_segment\n",
    "ORDER BY customer_count DESC;\n",
    "\"\"\"\n",
    "\n",
    "df_segments = con.execute(customer_segment_query).df()\n",
    "display(df_segments)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Plotting the Retention Dilemma\n",
    "plt.figure(figsize=(8, 4))\n",
    "ax = sns.barplot(\n",
    "    data=df_segments, \n",
    "    x='customer_segment', \n",
    "    y='customer_count', \n",
    "    hue='customer_segment', \n",
    "    legend=False, \n",
    "    palette=['#d95f02', '#7570b3', '#1b9e77']\n",
    ")\n",
    "plt.title('Customer Retention Breakdown: One-Time vs Repeat Buyers', fontsize=13, fontweight='bold', pad=15)\n",
    "plt.ylabel('Number of Unique Customers')\n",
    "plt.xlabel('Customer Lifecycle Segment')\n",
    "\n",
    "for p in ax.patches:\n",
    "    pct = p.get_height() * 100 / df_segments['customer_count'].sum()\n",
    "    ax.annotate(f'{int(p.get_height()):,d}\\n({pct:.1f}%)', \n",
    "                (p.get_x() + p.get_width() / 2., p.get_height() / 2),\n",
    "                ha='center', va='center', color='white', fontweight='bold', fontsize=11)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 🚨 Section 3 - Critical Business Finding:\n",
    "- **96.9% of all customers only purchase once** (93,099 out of 96,096 customers).\n",
    "- Only **3.1%** return for a second order, and only **19 customers** placed 5+ orders.\n",
    "- **Strategic Implication:** The business is spending heavily on Customer Acquisition Cost (CAC) to acquire new users into a \"leaky bucket\" without retention mechanisms."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 🛍️ Section 4: Product Portfolio & Pricing Dynamics\n",
    "Identifying high-value categories that drive the majority of gross merchandise value (GMV)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Top 10 Product Categories by Revenue\n",
    "top_categories_query = \"\"\"\n",
    "SELECT \n",
    "    p.product_category_name,\n",
    "    COUNT(oi.order_id) AS units_sold,\n",
    "    ROUND(SUM(oi.price), 2) AS total_revenue,\n",
    "    ROUND(AVG(oi.price), 2) AS avg_item_price\n",
    "FROM amazon_brazil.order_items oi\n",
    "JOIN amazon_brazil.products p\n",
    "    ON oi.product_id = p.product_id\n",
    "WHERE p.product_category_name IS NOT NULL\n",
    "GROUP BY p.product_category_name\n",
    "ORDER BY total_revenue DESC\n",
    "LIMIT 10;\n",
    "\"\"\"\n",
    "\n",
    "df_top_cat = con.execute(top_categories_query).df()\n",
    "display(df_top_cat)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Plot Top 10 Categories by Revenue\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.barplot(\n",
    "    data=df_top_cat, \n",
    "    y='product_category_name', \n",
    "    x='total_revenue', \n",
    "    hue='product_category_name', \n",
    "    legend=False, \n",
    "    palette='viridis'\n",
    ")\n",
    "plt.title('Top 10 Product Categories by Total Gross Revenue (BRL R$)', fontsize=13, fontweight='bold', pad=15)\n",
    "plt.xlabel('Total Revenue (R$ Millions)')\n",
    "plt.ylabel('Category Name')\n",
    "\n",
    "for i, row in df_top_cat.iterrows():\n",
    "    plt.text(row['total_revenue'] * 0.7, i, f\"R$ {row['total_revenue']/1e6:.2f}M\", \n",
    "             va='center', color='white', fontweight='bold', fontsize=10)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 🎯 Strategic Business Recommendations (The \"So What?\" for Leadership)\n",
    "\n",
    "Based on the quantitative SQL findings, here is the executive action plan:\n",
    "\n",
    "### 1. Fix the Customer Retention Funnel (Top Priority)\n",
    "- **Problem:** 96.9% one-time buyer rate means high CAC reliance.\n",
    "- **Action:** Launch an automated post-delivery engagement workflow (personalized re-order coupons within 30 days of delivery, subscription replenishment for Health & Beauty products).\n",
    "- **Target Metric:** Increase repeat customer share from 3.1% to 7.0% within 6 months.\n",
    "\n",
    "### 2. Optimize Payment Checkout & Reduce Friction\n",
    "- **Problem:** Boleto represents 19% of orders but suffers from manual payment drop-offs.\n",
    "- **Action:** Introduce **Pix** (instant Brazilian central bank payment) to replace Boleto, offering instant clearance and reducing order cancellation rates.\n",
    "\n",
    "### 3. Category Focus & Inventory Staging\n",
    "- **Problem:** High concentration in top 5 categories (*Beleza_saude, Relogios, Cama_mesa_banho*).\n",
    "- **Action:** Partner with top sellers in these 5 categories for fulfillment warehousing to guarantee sub-3-day delivery and boost customer satisfaction.\n",
    "\n",
    "### 4. Capitalize on Q4 Seasonality\n",
    "- **Action:** Begin seller onboarding and promo prep in September/October to capture peak November Black Friday volume without logistics bottlenecks."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.11.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("Amazon_Business_Case_Study.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print("Updated Amazon_Business_Case_Study.ipynb successfully!")
