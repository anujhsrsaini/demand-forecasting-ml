# Executive Summary: Demand Forecasting ML Project

**Author:** Anuj Saini, Lead Data Analyst  
**Date:** July 14, 2026  

This project translates a vague operational requirement ("optimize inventory to prevent stock-outs and over-ordering") into a structured, production-ready machine learning forecasting pipeline. 

### Key Takeaways

1.  **Macro Decay Trend & Category Uniformity:** 
    Exploratory analysis of 106,205 ordered units over a 13-week period revealed a massive **76.4% systemic drop** in demand from a peak of 14,006 units (week of April 6) to 3,302 units (week of June 8). The decline was remarkably uniform across all 14 categories (varying between **-73.7%** and **-80.6%** change), suggesting a company-wide driver rather than shifting consumer product preferences.
2.  **Evaluating the Accuracy Frontier (16.14% WMAPE):** 
    We implemented a leak-free recursive forecasting pipeline evaluated via 3-fold expanding window cross-validation over a 4-week horizon. The **Gradient Boosting Regressor** achieved a **16.14% mean WMAPE**, delivering a **15.54% relative lift** over the Naive Baseline (19.11% WMAPE) and providing operations with a robust tool to calculate safety stock.
3.  **Linear Regression Recursive Collapse:** 
    A simple Linear Regression model appeared highly accurate in standard static training tests (~7.2% training error). However, when evaluated in a recursive, multi-step production-like environment, it completely collapsed, yielding a catastrophic **70.43% WMAPE**. This failure highlights the necessity of non-parametric tree ensembles for multi-step recursive forecasting on short historical datasets.
