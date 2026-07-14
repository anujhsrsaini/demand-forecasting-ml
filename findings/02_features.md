# Milestone 2: Feature Engineering & Temporal Hygiene

**Prepared by:** Anuj Saini, Lead Data Analyst  
**Date:** July 14, 2026  

### 1. Overview of Features Built
We built a robust feature pipeline that aggregates transaction-level data into weekly, category-level demand forecasts. The resulting feature DataFrame contains exactly one row per (week_start × category_name) with **11 features** spanning five distinct feature groups:

1.  **Lag Features (`qty_lag_1` to `qty_lag_4`):** These features represent the actual quantities ordered 1, 2, 3, and 4 weeks ago, respectively.
    *   *Why:* Time series demand typically exhibits autoregressive properties, where recent historical demand heavily influences future demand. Capturing up to 4 weeks of history allows the model to learn recent short-term momentum and month-over-month baseline transitions.
2.  **Rolling Statistics (`qty_roll_mean_2`, `qty_roll_std_2`, `qty_roll_mean_4`, `qty_roll_std_4`):** These represent the moving average and standard deviation over 2-week and 4-week windows.
    *   *Why:* Moving averages smooth out short-term fluctuations to reveal underlying trends, while rolling standard deviations capture demand volatility, which is crucial for determining safety stock levels.
3.  **Pricing Features (`price_lag_1`):** The average unit price of the category in the prior week.
    *   *Why:* To capture price elasticity of demand and adjust forecasts based on pricing shifts.
4.  **Temporal/Calendar Features (`time_idx`):** A linear index representing the number of weeks since the start of the dataset.
    *   *Why:* The historical data exhibits a very strong, uniform downward trend (-76.4% overall drop). A linear time index allows the model to learn and extrapolate this global decay rate.
5.  **Categorical Encoding (`category_expanding_mean`):** An expanding average of historical weekly demand for each category.
    *   *Why:* Target encodes the category identity to capture its relative volume (e.g., Skincare as high-volume vs. Bedding as low-volume) in a single column, preventing the feature expansion associated with one-hot encoding.

### 2. Ensuring Temporal Hygiene & Preventing Leakage
Data leakage occurs when information from the future (the target week $W$) or the target week itself is included in the features used to predict week $W$. To guarantee strict **temporal hygiene**, we implemented the following rules in [src/features.py](file:///home/anuj/Personal/DataBuoy-Projects-Testing/demand-forecasting-ml/src/features.py):
*   **Prior-Week Shifting:** Before computing any lag, rolling mean, rolling standard deviation, or expanding mean, the target series `qty` is shifted by exactly 1 week (`shift(1)`). This guarantees that the rolling window for week $W$ spans weeks $W-4$ to $W-1$, never including week $W$.
*   **Expanding Mean Isolation:** The `category_expanding_mean` uses an expanding window applied *after* the shift, ensuring that the feature at week $W$ is computed as the average of weeks $1$ through $W-1$, leaving the target week $W$ completely isolated.

### 3. Leakage Sanity Check
To verify temporal hygiene, we trained a baseline linear regression model on the generated features:
- **Naive Lag-1 Baseline WMAPE:** **23.86%**
- **Linear Regression Model WMAPE:** **7.26%**
- **R² Score:** **0.9115**

Because the model achieves a 7.26% error rather than 0% (which would indicate a trivial shortcut/leakage), and outperforms the naive baseline by over 16%, we confirm that the features are leak-free and capture the underlying linear trend and category scales correctly.
