# Demand Forecasting Machine Learning Project

**Author:** Anuj Saini  
**Repository:** `https://github.com/anujhsrsaini/demand-forecasting-ml`

---

## Project Overview
This repository contains a complete, end-to-end machine learning solution designed to translate vague inventory planning questions ("how do we prevent stock-outs and over-ordering?") into a precise, mathematically rigorous forecasting pipeline. Leveraging transaction data from a PostgreSQL database, the pipeline aggregates demand to the product category level and recursive-forecasts weekly unit demand over a 4-week horizon (weeks $t+1$ to $t+4$). 

Exploratory analysis of 13 weeks of sales history (106,205 units sold) revealed a severe, highly uniform downward trend across all 14 categories (varying between -73.7% and -80.6% change). To address this, we engineered features under strict temporal hygiene and built a recursive forecasting engine. Our final **Gradient Boosting Regressor** achieves a **16.14% mean WMAPE**, representing a **15.54% relative lift** over the Naive Baseline.

### Recursive Forecast vs. Naive Baseline (Skincare Category)
Below is the embedded prediction-vs-actual chart demonstrating the model's recursive forecasting performance on the test fold relative to the naive baseline:

![Forecast Comparison](notebooks/model_predictions_comparison.png)

---

## Repository Structure

*   `notebooks/`
    *   [01_explore.ipynb](notebooks/01_explore.ipynb): Exploration of the demand time series, trend analysis, and initial category correlation.
    *   [02_features.ipynb](notebooks/02_features.ipynb): Feature engineering pipeline and leakage checks.
    *   [03_models.ipynb](notebooks/03_models.ipynb): Cross-validation splits, training, recursive forecasting, and evaluation.
*   `findings/`
    *   [00_executive_summary.md](findings/00_executive_summary.md): 3-takeaway project summary with metrics.
    *   [01_problem_framing.md](findings/01_problem_framing.md): Business framing, target variable, granularity, and evaluation metric choice.
    *   [02_features.md](findings/02_features.md): Rationale behind features and temporal hygiene explanation.
    *   [03_model_comparison.md](findings/03_model_comparison.md): Cross-validation results and model comparisons.
    *   [04_production_plan.md](findings/04_production_plan.md): Operational production, monitoring, and retraining strategy.
*   `src/`
    *   [features.py](src/features.py): Reusable feature engineering code path.
*   `requirements.txt`: Python dependencies.

---

## Tech Stack & Tools Used
*   **Database:** PostgreSQL (Supabase) via SQLAlchemy
*   **Data Wrangling:** Pandas, NumPy
*   **Visualization:** Matplotlib, Seaborn
*   **Machine Learning:** Scikit-Learn (LinearRegression, RandomForestRegressor, GradientBoostingRegressor)
*   **Version Control:** Git, GitHub CLI (`gh`)

---

## How to Reproduce

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/anujhsrsaini/demand-forecasting-ml.git
    cd demand-forecasting-ml
    ```
2.  **Set up the environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Configure credentials:**
    Create a `.env` file in the root directory and add your database connection details:
    ```text
    Host=your-database-host-url
    Port=5432
    Database=postgres
    Schema=ecom
    Username=your-read-only-username
    Password=your-read-only-password
    ```
4.  **Run the notebooks:**
    Launch Jupyter or run the notebooks sequentially via `jupyter nbconvert --execute --inplace notebooks/*.ipynb`.

---

## What I'd Do Next
*   **Hierarchical Forecasting Reconciliation (MinT):** Currently, we forecast at the category level and assume a simple top-down proportions method to distribute forecasts to SKUs. To optimize, I would implement **Minimum Trace (MinT)** reconciliation to produce coherent forecasts at both the SKU and Category level simultaneously, minimizing total variance.
*   **Cold-Start Strategy for New Products:** We would implement a metadata-based similarity pipeline (e.g., using product descriptions and tags embedded via TF-IDF or Word2Vec) to automatically assign proxy demand to newly launched products during their first 4 weeks.
