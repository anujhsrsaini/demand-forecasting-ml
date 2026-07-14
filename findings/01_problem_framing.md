## Executive Brief: Demand Forecasting Problem Framing

**Prepared for:** Operations Director  
**Prepared by:** Anuj Saini, Lead Data Analyst  
**Date:** July 14, 2026  

### 1. Business Context & Problem Statement
To optimize inventory management, minimize stock-outs, and prevent capital lockup in over-stocking, we must translate our general forecasting goal into a concrete, solvable machine learning task. 

Our precise problem statement is:
> **Predict weekly demand (total quantity ordered) at the product category level for a 4-week horizon (weeks $t+1$ to $t+4$), evaluated by Weighted Mean Absolute Percentage Error (WMAPE).**

### 2. Analytical Framing & Rationale

*   **Target Variable:** The target variable is the weekly sum of ordered quantities (`qty`) rather than sales revenue. Inventory planning is concerned with physical storage capacity and item counts, which are directly dictated by unit quantities.
*   **Granularity:** Forecasting will be conducted at the **Product Category** level (14 distinct categories). The historical dataset contains 12,077 unique product variants (SKUs) but only 106,205 total units sold over 13 weeks. This equates to an average of fewer than 9 units per SKU over the entire period, making SKU-level data extremely sparse and noisy. Aggregating to the category level (e.g., Skincare, Shoes) provides dense, stable time series with thousands of units per week, making the forecasting problem statistically tractable. A top-down allocation method can later distribute the category-level forecasts to individual SKUs based on historical proportions.
*   **Horizon:** We define a **4-week forecasting horizon** (predicting weeks $t+1$ to $t+4$ relative to the current week $t$). A 4-week window aligns with standard supplier lead times, providing operations with sufficient time to place purchase orders and adjust warehouse allocations.
*   **Evaluation Metric:** We will use **Weighted Mean Absolute Percentage Error (WMAPE)** as our primary metric:
    $$\text{WMAPE} = \frac{\sum_{i} |y_i - \hat{y}_i|}{\sum_{i} y_i}$$
    WMAPE is business-interpretable (expressed as a percentage error) but avoids the division-by-zero and near-zero explosion issues of standard MAPE. Crucially, it scales errors by actual volume, ensuring that forecasting errors in high-volume categories like Skincare impact the metric more than errors in low-volume categories like Bedding. We will also monitor **Root Mean Squared Error (RMSE)** to flag and minimize large outlier errors that could trigger critical stock-outs.

### 3. Historical Demand Analysis
Our analysis of the 13 weeks of historical data (March 16, 2026 – June 14, 2026) reveals several key dynamics:
*   **Trend:** The overall time series exhibits a severe, continuous downward trend. Total weekly demand starts at 11,640 units, peaks in the week of April 6 at 14,006 units, and then steadily drops to 3,302 units in the final week (June 8)—a **76.4% decline** from the peak.
*   **Uniformity:** This decline is remarkably uniform across all 14 categories, with drops from the peak week to the last week ranging tightly between **-73.7%** (Jeans) and **-80.6%** (Headphones). This uniformity indicates a systemic macro-driver (e.g., scaling down launch marketing campaigns, technical site issues, or decaying cohort engagement) rather than organic shifts in consumer preferences.
*   **Seasonality & Volatility:** Due to the short 13-week historical window, yearly seasonality cannot be observed or learned. Volatility is high in the first four weeks but stabilizes into a steady decay pattern thereafter.

### 4. Key Constraints & Risks
*   **Extremely Short History:** 13 weeks is insufficient to learn yearly seasonal cycles (e.g., holidays, weather-driven demands), which is a major limitation for long-term planning.
*   **Permanent vs. Cyclical Trend:** The models may struggle to differentiate between a permanent business decline and a temporary post-promotional slump.
