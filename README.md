```markdown
# 🌿 CarbonSight — Carbon Credit Price Predictor

Predicts whether EU carbon credit prices will go **up or down** next week,
and explains *why* using explainable AI.

---

## What This Project Does

Carbon credits are permits that let companies emit CO₂. Their price changes
every week based on energy markets, climate news, and global policy events.

This project:
- Collects and cleans 10 years of weekly carbon market data (2015–2026)
- Analyses what actually drives carbon price movements
- Builds a machine learning model to predict next week's % price change
- Explains every prediction using SHAP (so you know *why*, not just *what*)
- Deploys everything as a live web app

---

## The Question Being Answered

> *Do gas prices, CO₂ levels, market fear (VIX), and COP summit proximity
> explain weekly carbon price movements — and can we predict them?*

---

## Key Findings

- **Momentum is the strongest driver.** Recent price trends predict future
  price direction better than any external factor.
- **Gas prices don't move carbon prices week to week.** The relationship
  only exists at a long-term trend level, not short-term.
- **CO₂ concentration is not a useful predictor.** It trends upward slowly
  alongside carbon prices but carries zero weekly signal.
- **COP summits cause post-summit price jumps, not pre-summit run-ups.**
  COP26 Glasgow caused the biggest single rally (+€12 after the summit).
- **2021 was a structural break.** Carbon prices went from ~€25 to €80+
  after the EU Green Deal. Pre-2021 and post-2021 are different markets.

---

## Model Performance

| Model | R² | Directional Accuracy |
|---|---|---|
| Lasso | 0.19 | 62.4% |
| XGBoost | 0.16 | **63.0%** |
| Ridge | 0.15 | 60.7% |
| Random Forest | 0.13 | 60.7% |
| Baseline (always predict mean) | -0.03 | 49.1% |

The model predicts market direction correctly ~63% of the time.
Random guessing gives 50% — so this is a meaningful improvement.

---

## Project Structure

```
carbon-credit-predictor/
│
├── notebooks/
│   ├── 01_Data_Collection.ipynb
│   ├── 02_EDA_and_DA.ipynb
│   ├── 03_Feature_Engineering.ipynb
│   ├── 04_XAI_Analysis.ipynb
│   └── 05_Model_Training.ipynb
│
├── models/
│   ├── xgb_tuned.pkl
│   └── scaler.pkl
│
├── frontend/          ← Streamlit app
├── backend/           ← FastAPI backend
└── data/
    └── processed/
        └── final_dataset_engineered.csv
```

---

## Data Sources

| Data | Source |
|---|---|
| EU Carbon Futures prices | Investing.com |
| Natural Gas prices | U.S. EIA |
| Atmospheric CO₂ | NOAA |
| Market Fear Index (VIX) | CBOE / Yahoo Finance |
| COP Summit dates | UNFCCC |

Weekly data from April 2015 to April 2026 — 577 observations.

