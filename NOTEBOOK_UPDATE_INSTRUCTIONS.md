# Notebook Update Instructions for RF 22 Features

## Summary of Changes

All thesis LaTeX files and MODEL_RESULTS have been updated to reflect **22 final Random Forest features** (removed `lk_lag_1` and `fur_1500_high_rolling_mean_7` from the original 24).

## Files Already Updated ✅

1. `MODEL_RESULTS_COMPLETE.md` - Updated to 22 features with correct breakdown
2. `research_thesis/chapters/Methodology.tex` - Updated RF 273→22 pipeline
3. `research_thesis/chapters/Results.tex` - Updated feature ranges
4. `THESIS_REVIEW_REPORT.md` - Updated to 22 features
5. `SUPERVISOR_QA_GUIDE.md` - Updated to 22 features with new percentages

## Manual Notebook Updates Needed

### 1. Generate_Thesis_Figures.ipynb

**Location:** Find the cell titled "Figure 4.12: Top 20 Features by Random Forest Importance"

**Change the title to:**

```markdown
## Figure 4.12: Top 22 Features by Random Forest Importance (Final Selected Features)

This figure shows the 22 final features selected for the Random Forest model after removing non-transport fuel features (kerosene and furnace oil). Only diesel (LAD) is retained for fuel features as it's relevant for agricultural transport costs.
```

**Replace the `features_importance` dictionary with the 22 final features:**

```python
# 22 final features with combined scores from MODEL_RESULTS_COMPLETE.md
features_importance = {
    'bandarawela_supply_factor_rolling_mean_7': 0.895,
    'pussellawa_supply_factor_rolling_mean_14': 0.252,
    'bandarawela_supply_factor_rolling_mean_14': 0.218,
    'yatawaththa_supply_factor_rolling_mean_14': 0.195,
    'is_dambulla_increase': 0.173,
    'mandaramnuwara_mean_precipitation_mm_lag_7': 0.167,
    'mandaramnuwara_mean_precipitation_mm_rolling_sum_7': 0.166,
    'kalpitiya_mean_precipitation_mm_lag_7': 0.165,
    'marassana_mean_precipitation_mm_lag_1': 0.164,
    'mandaramnuwara_mean_precipitation_mm_rolling_sum_14': 0.163,
    'kalpitiya_mean_precipitation_mm_rolling_sum_7': 0.163,
    'kandapola_mean_precipitation_mm': 0.162,
    'jaffna_mean_precipitation_mm': 0.157,
    'mandaramnuwara_mean_precipitation_mm_lag_3': 0.147,
    'kandapola_supply_factor_rolling_mean_14': 0.142,
    'kalpitiya_mean_precipitation_mm_rolling_sum_14': 0.125,
    'quarter': 0.109,
    'precip_central_highland_mean': 0.097,
    'lad_lag_1': 0.061,  # Diesel (transport fuel) - KEPT
    'price_rolling_mean_30': 0.049,
    'price_lag_14': 0.046,
    'precip_uva_province_sum': 0.045
}
```

**Update the color-coding logic to match the new features:**

```python
# Color code by category
colors = []
for feat in feature_df['Feature']:
    if 'price' in feat.lower():
        colors.append('#2E86AB')  # Blue for price features
    elif any(weather in feat for weather in ['precipitation', 'precip']):
        colors.append('#06A77D')  # Green for weather features
    elif any(market in feat for market in ['dambulla', 'demand', 'market']):
        colors.append('#F77F00')  # Orange for market features
    elif 'supply' in feat.lower():
        colors.append('#D62828')  # Red for supply features
    elif any(fuel in feat.lower() for fuel in ['lad', 'diesel']):
        colors.append('#9D4EDD')  # Purple for fuel features (diesel only)
    else:
        colors.append('#6C757D')  # Gray for temporal features (quarter)
```

**Update the legend with new percentages:**

```python
legend_elements = [
    Patch(facecolor='#06A77D', edgecolor='black', label='Weather Features (54.5%)'),
    Patch(facecolor='#D62828', edgecolor='black', label='Supply Features (22.7%)'),
    Patch(facecolor='#2E86AB', edgecolor='black', label='Price Features (9.1%)'),
    Patch(facecolor='#9D4EDD', edgecolor='black', label='Fuel Features (4.5% - Diesel only)'),
    Patch(facecolor='#F77F00', edgecolor='black', label='Market Features (4.5%)'),
    Patch(facecolor='#6C757D', edgecolor='black', label='Temporal Features (4.5%)')
]
```

**Update the title:**

```python
ax.set_title('Top 22 Features by Random Forest Importance (Final Selected)', fontsize=14, fontweight='bold')
```

**Update the print statements:**

```python
print("Figure 4.12 saved: research-thesis/figures/feature_importance_rf.png")
print(f"\nTop 3 Features (22 final features after fuel refinement):")
print(f"1. {feature_df.iloc[-1]['Feature']}: {feature_df.iloc[-1]['Importance']:.3f}")
print(f"2. {feature_df.iloc[-2]['Feature']}: {feature_df.iloc[-2]['Importance']:.3f}")
print(f"3. {feature_df.iloc[-3]['Feature']}: {feature_df.iloc[-3]['Importance']:.3f}")
print(f"Top 3 combined: {feature_df.iloc[-3:]['Importance'].sum():.1%} of total importance")
print(f"\nNote: Removed lk_lag_1 (kerosene) and fur_1500_high_rolling_mean_7 (furnace oil)")
print(f"      Kept only transport-relevant fuel: lad_lag_1 (diesel)")
```

### 2. Random_Forest_Carrot_Price_Prediction.ipynb

**Location:** Find the cell with RFE intersection code (around line 570)

**Add this code after the intersection is created:**

```python
# Remove non-transport fuel features (kerosene and furnace oil)
# Keep only diesel (lad) and petrol (Lp_) for transport cost modeling
non_transport_fuel = ['lk_lag_1', 'fur_1500_high_rolling_mean_7']
selected_features_final = [f for f in selected_features_final if f not in non_transport_fuel]
print(f"\n🔧 FUEL REFINEMENT: Removed non-transport fuel features")
print(f"   Removed: {non_transport_fuel}")
print(f"✅ FINAL FEATURES (Transport-Relevant): {len(selected_features_final)}")
```

**Location:** Find the category breakdown section (around line 640)

**Update the Fuel category filter from:**

```python
'Fuel': [f for f in selected_features_final if any(x in f.lower() for x in ['fur', 'lp_', 'lad', 'lsd', 'lk'])],
```

**To:**

```python
'Fuel': [f for f in selected_features_final if any(x in f.lower() for x in ['lp_', 'lad', 'lsd'])],  # Removed 'fur' and 'lk'
```

**Also update the fuel_cols definition (around line 411) to remove references to lk and fur_1500_high:**

```python
# For feature engineering, keep all fuel columns initially
fuel_cols = [col for col in df.columns if 'fur_' in col or any(x in col for x in ['Lp_', 'lad', 'lsd', 'lk', 'lik'])]

# But note: lk and fur_1500_high will be removed in final feature selection
```

### 3. Update Final Feature Count References

Search all notebooks for:

- "24 features" → change to "22 features" (where referring to RF final features)
- "24 final features" → "22 final features"
- References to the removed features (`lk_lag_1`, `fur_1500_high_rolling_mean_7`)

## Feature Category Breakdown (Updated)

### Random Forest - 22 Final Features:

- **Weather Features:** 12 (54.5%)
- **Supply Features:** 5 (22.7%)
- **Price Features:** 2 (9.1%)
- **Fuel Features:** 1 (4.5%) - diesel only (`lad_lag_1`)
- **Market Features:** 1 (4.5%)
- **Temporal Features:** 1 (4.5%)

### LSTM - 8 Final Features (unchanged):

- **Market & Demand:** 4 (50.0%)
- **Price Features:** 3 (37.5%)
- **Fuel Prices:** 1 (12.5%)

## Rationale for Removal

**lk (kerosene):** Non-transport fuel used for lighting/cooking, not relevant for agricultural transport costs that drive carrot prices.

**fur_1500_high (furnace oil):** Industrial fuel not used in agricultural transport; irrelevant for vegetable market price modeling.

**Kept: lad_lag_1 (Diesel LAD - Auto Diesel):** Primary transport fuel for trucks moving carrots from farms to Dambulla market - directly relevant.

## Verification Checklist

After manual updates, verify:

- [ ] Generate_Thesis_Figures.ipynb updated with 22 features
- [ ] Random_Forest_Carrot_Price_Prediction.ipynb adds fuel refinement step
- [ ] Run Generate_Thesis_Figures.ipynb to regenerate figure
- [ ] New `feature_importance_rf.png` shows 22 features
- [ ] All "24 features" references changed to "22 features" in notebooks
- [ ] Thesis compiles without errors
- [ ] All figure numbers and references are correct

## Files to Regenerate

After updating notebooks, regenerate:

1. `research-thesis/figures/feature_importance_rf.png` (from Generate_Thesis_Figures.ipynb)
2. Re-run Random Forest notebook cells to update saved model artifacts
3. Recompile thesis LaTeX to verify all cross-references work

---

**Status:** Thesis LaTeX files are complete and consistent. Only notebook manual updates remain.
