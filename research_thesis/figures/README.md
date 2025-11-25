# Figures Directory

This directory contains all screenshots and figures for the thesis, particularly for Chapter 4 (Results and Discussion).

## Required Screenshots by Section

### 4.1 Exploratory Data Analysis

- `price_timeseries.png` - Daily carrot price trends (2020-2025)
- `price_rainfall_central.png` - Price vs Central Highland precipitation scatter plot
- `price_rainfall_uva.png` - Price vs Uva Province precipitation
- `price_rainfall_northern.png` - Price vs Northern region precipitation
- `price_diesel_lad.png` - Price vs Diesel (LAD) scatter plot
- `price_petrol_lp95.png` - Price vs Petrol (LP 95) scatter plot
- `seasonal_decomp.png` - Four-panel seasonal decomposition plot

### 4.3 Feature Selection Results

- `feature_selection_stages.png` - Bar chart: RF (273 → 80 → 58 → 14), LSTM (163 → 19 features)
- `correlation_heatmap.png` - 19×19 correlation heatmap

### 4.5 ARIMA Results

- `arima_diagnostics.png` - Four-panel ARIMA diagnostic plot

### 4.6 LSTM Results

- `bidirectional_lstm_training.png` - Training history (Loss and MAPE curves)

### 4.8 Feature Importance Analysis

- `feature_importance_rf.png` - Top 20 features horizontal bar chart

### 4.9 Ablation Study

- `ablation_study.png` - Bar chart showing MAPE increase by category removal

### 4.10 SHAP Analysis

- `shap_summary.png` - SHAP beeswarm plot
- `shap_dependence_price.png` - SHAP dependence plot for price_lag_1
- `shap_dependence_weather.png` - SHAP dependence for Central Highland precipitation

### 4.11 Predictions Visualization

- `predictions_bidirectional.png` - Actual vs predicted prices across all splits

### 4.13 AI Agent

- `agent_architecture.png` - 3-tier architecture diagram
- `gradio_interface.png` - Gradio web interface screenshot

## File Naming Convention

- Use lowercase with underscores
- Include descriptive names matching figure labels in Results.tex
- Preferred formats: PNG (for screenshots), PDF (for vector graphics)
- Recommended resolution: 300 DPI for publication quality

## Total Screenshots Needed

Approximately 18-20 figures for complete Results chapter visualization.
