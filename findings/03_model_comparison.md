# Milestone 3: Model Training, Evaluation, and Comparison

**Prepared by:** Anuj Saini, Lead Data Analyst  
**Date:** July 14, 2026  

### 1. Evaluation Methodology & Temporal Hygiene
To ensure a rigorous and honest comparison, we evaluated all models using **Expanding Window Time-Series Cross-Validation**. Given our 13-week historical window, we allocated the first 4 weeks (weeks 0–3) for feature initialization and trained on expanding windows starting from week 4. We tested each model on a **4-week forecast horizon** (matching our business requirement), yielding three distinct evaluation folds:
*   **Fold 1:** Train on weeks 4–6, validate on weeks 7–10
*   **Fold 2:** Train on weeks 4–7, validate on weeks 8–11
*   **Fold 3:** Train on weeks 4–8, validate on weeks 9–12

To evaluate the ML models over the 4-week horizon, we implemented a **recursive forecasting pipeline**. Instead of using actual prior-week demand values during the test window (which would cause data leakage, as they are unavailable in production), the models recursively feed their own predictions back as lag features to generate subsequent forecasts.

### 2. Model Definitions
1.  **Naive Baseline:** Carries forward the last known actual demand (from week $T$) as a constant forecast for all weeks in the test horizon ($T+1$ to $T+4$). Since we lack a full year of history to use a seasonal naive baseline, this represents the most honest static benchmark.
2.  **Linear Regression:** A parametric baseline capturing linear trends and additive relationships.
3.  **Random Forest:** A non-parametric ensemble of 100 decision trees (max depth 4) to capture non-linear interactions.
4.  **Gradient Boosting:** A boosted ensemble of 50 regression trees (max depth 3, learning rate 0.1) designed to sequentially correct prediction errors.

### 3. Honest Evaluation Results (WMAPE)
The table below details the performance of each model across the cross-validation folds:

| Model | Fold 1 WMAPE | Fold 2 WMAPE | Fold 3 WMAPE | Mean WMAPE | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Naive Baseline** | 12.80% | 18.10% | 26.42% | **19.11%** | 5.60% |
| **Linear Regression** | 106.20% | 60.53% | 44.55% | **70.43%** | 26.12% |
| **Random Forest** | 15.53% | 14.55% | 24.68% | **18.25%** | 4.56% |
| **Gradient Boosting** | **15.54%** | **12.56%** | **20.32%** | **16.14%** | 6.47% |

*Note: Fold-by-fold results show that Gradient Boosting achieves a **16.14% mean WMAPE**, representing a **15.54% relative error reduction (lift)** over the Naive Baseline (19.11% WMAPE).*

### 4. Key Analytical Insights & Diagnosis
*   **Linear Regression Feedback Instability:** While Linear Regression achieved a very low error on the training set (~7.2%), it completely collapsed under recursive forecasting, yielding a catastrophic **70.43% WMAPE**. Because training windows are short (only 3–5 weeks), the regression coefficients were highly unstable. When the model recursively fed its own predictions back, the negative lag coefficients (e.g., `qty_lag_2` at -0.34) caused wild oscillations and diverging errors.
*   **Gradient Boosting Robustness:** Gradient Boosting proved highly robust, achieving the lowest overall error (16.14% mean WMAPE). Because tree-based models constrain predictions to the range of training data, they do not suffer from the runaway divergence seen in linear regression.
*   **Feature Interpretability:** Analysis of the Gradient Boosting feature importances reveals that:
    1.  `qty_roll_mean_2` (recent volume level) accounts for **46.2%** of predictive importance.
    2.  `time_idx` (linear week index) accounts for **30.6%**.
    3.  `category_expanding_mean` (baseline volume) accounts for **8.8%**.
    
    Together, these three features represent **85.6%** of the model's decision-making power, demonstrating that demand is primarily driven by a category's base volume adjusted by recent velocity and the overall systemic downward trend.
