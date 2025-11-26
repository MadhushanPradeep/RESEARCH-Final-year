#!/usr/bin/env python3
"""
Script to update Generate_Thesis_Figures.ipynb with 22 final RF features
Run this script to update the notebook automatically.
"""

import json
import sys

def update_notebook():
    notebook_path = 'Generate_Thesis_Figures.ipynb'
    
    try:
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Find and update the relevant cells
        for cell in notebook['cells']:
            # Update markdown cell title
            if cell['cell_type'] == 'markdown' and any('Figure 4.12: Top 20 Features' in line for line in cell.get('source', [])):
                cell['source'] = [
                    "## Figure 4.12: Top 22 Features by Random Forest Importance (Final Selected Features)\n",
                    "\n",
                    "This figure shows the 22 final features selected for the Random Forest model after removing non-transport fuel features (kerosene and furnace oil). Only diesel (LAD) is retained for fuel features as it's relevant for agricultural transport costs.\n"
                ]
                print("✓ Updated markdown cell title")
            
            # Update the Python cell with feature importance data
            if cell['cell_type'] == 'code' and any('features_importance = {' in line for line in cell.get('source', [])):
                # Check if this is the right cell (contains the old feature list)
                source_str = ''.join(cell.get('source', []))
                if "'price_lag_1': 0.185" in source_str or "'Diesel_LAD'" in source_str:
                    # Replace the entire cell content
                    cell['source'] = [
                        "# Generate Random Forest feature importance plot\n",
                        "# This shows the 22 final selected features (after removing lk_lag_1 and fur_1500_high_rolling_mean_7)\n",
                        "# Based on MODEL_RESULTS_COMPLETE.md - Final Selected Features (22 features)\n",
                        "\n",
                        "# 22 final features with combined scores\n",
                        "features_importance = {\n",
                        "    'bandarawela_supply_factor_rolling_mean_7': 0.895,\n",
                        "    'pussellawa_supply_factor_rolling_mean_14': 0.252,\n",
                        "    'bandarawela_supply_factor_rolling_mean_14': 0.218,\n",
                        "    'yatawaththa_supply_factor_rolling_mean_14': 0.195,\n",
                        "    'is_dambulla_increase': 0.173,\n",
                        "    'mandaramnuwara_mean_precipitation_mm_lag_7': 0.167,\n",
                        "    'mandaramnuwara_mean_precipitation_mm_rolling_sum_7': 0.166,\n",
                        "    'kalpitiya_mean_precipitation_mm_lag_7': 0.165,\n",
                        "    'marassana_mean_precipitation_mm_lag_1': 0.164,\n",
                        "    'mandaramnuwara_mean_precipitation_mm_rolling_sum_14': 0.163,\n",
                        "    'kalpitiya_mean_precipitation_mm_rolling_sum_7': 0.163,\n",
                        "    'kandapola_mean_precipitation_mm': 0.162,\n",
                        "    'jaffna_mean_precipitation_mm': 0.157,\n",
                        "    'mandaramnuwara_mean_precipitation_mm_lag_3': 0.147,\n",
                        "    'kandapola_supply_factor_rolling_mean_14': 0.142,\n",
                        "    'kalpitiya_mean_precipitation_mm_rolling_sum_14': 0.125,\n",
                        "    'quarter': 0.109,\n",
                        "    'precip_central_highland_mean': 0.097,\n",
                        "    'lad_lag_1': 0.061,\n",
                        "    'price_rolling_mean_30': 0.049,\n",
                        "    'price_lag_14': 0.046,\n",
                        "    'precip_uva_province_sum': 0.045\n",
                        "}\n",
                        "\n",
                        "# Create DataFrame\n",
                        "feature_df = pd.DataFrame(list(features_importance.items()), columns=['Feature', 'Importance'])\n",
                        "feature_df = feature_df.sort_values('Importance', ascending=True)  # Sort for horizontal bar chart\n",
                        "\n",
                        "# Create horizontal bar chart\n",
                        "fig, ax = plt.subplots(figsize=(12, 10))\n",
                        "\n",
                        "# Color code by category\n",
                        "colors = []\n",
                        "for feat in feature_df['Feature']:\n",
                        "    if 'price' in feat.lower():\n",
                        "        colors.append('#2E86AB')  # Blue for price features\n",
                        "    elif any(weather in feat for weather in ['precipitation', 'precip']):\n",
                        "        colors.append('#06A77D')  # Green for weather features\n",
                        "    elif any(market in feat.lower() for market in ['dambulla', 'demand', 'market']):\n",
                        "        colors.append('#F77F00')  # Orange for market features\n",
                        "    elif 'supply' in feat.lower():\n",
                        "        colors.append('#D62828')  # Red for supply features\n",
                        "    elif any(fuel in feat.lower() for fuel in ['lad', 'diesel']):\n",
                        "        colors.append('#9D4EDD')  # Purple for fuel features (diesel only)\n",
                        "    else:\n",
                        "        colors.append('#6C757D')  # Gray for temporal features (quarter)\n",
                        "\n",
                        "bars = ax.barh(feature_df['Feature'], feature_df['Importance'], color=colors, edgecolor='black', linewidth=0.7)\n",
                        "\n",
                        "# Add value labels on bars\n",
                        "for i, (feat, imp) in enumerate(zip(feature_df['Feature'], feature_df['Importance'])):\n",
                        "    ax.text(imp + 0.015, i, f'{imp:.3f}', va='center', fontsize=9, fontweight='bold')\n",
                        "\n",
                        "ax.set_xlabel('Feature Importance', fontsize=13, fontweight='bold')\n",
                        "ax.set_ylabel('Feature', fontsize=13, fontweight='bold')\n",
                        "ax.set_title('Top 22 Features by Random Forest Importance (Final Selected)', fontsize=14, fontweight='bold')\n",
                        "ax.grid(axis='x', alpha=0.3, linestyle='--')\n",
                        "\n",
                        "# Add legend\n",
                        "from matplotlib.patches import Patch\n",
                        "legend_elements = [\n",
                        "    Patch(facecolor='#06A77D', edgecolor='black', label='Weather Features (54.5%)'),\n",
                        "    Patch(facecolor='#D62828', edgecolor='black', label='Supply Features (22.7%)'),\n",
                        "    Patch(facecolor='#2E86AB', edgecolor='black', label='Price Features (9.1%)'),\n",
                        "    Patch(facecolor='#9D4EDD', edgecolor='black', label='Fuel Features (4.5% - Diesel only)'),\n",
                        "    Patch(facecolor='#F77F00', edgecolor='black', label='Market Features (4.5%)'),\n",
                        "    Patch(facecolor='#6C757D', edgecolor='black', label='Temporal Features (4.5%)')\n",
                        "]\n",
                        "ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.9)\n",
                        "\n",
                        "plt.tight_layout()\n",
                        "plt.savefig('research-thesis/figures/feature_importance_rf.png', dpi=300, bbox_inches='tight')\n",
                        "print(\"Figure 4.12 saved: research-thesis/figures/feature_importance_rf.png\")\n",
                        "print(f\"\\nTop 3 Features (22 final features after fuel refinement):\")\n",
                        "print(f\"1. {feature_df.iloc[-1]['Feature']}: {feature_df.iloc[-1]['Importance']:.3f}\")\n",
                        "print(f\"2. {feature_df.iloc[-2]['Feature']}: {feature_df.iloc[-2]['Importance']:.3f}\")\n",
                        "print(f\"3. {feature_df.iloc[-3]['Feature']}: {feature_df.iloc[-3]['Importance']:.3f}\")\n",
                        "print(f\"Top 3 combined: {feature_df.iloc[-3:]['Importance'].sum():.1%} of total importance\")\n",
                        "print(f\"\\nNote: Removed lk_lag_1 (kerosene) and fur_1500_high_rolling_mean_7 (furnace oil)\")\n",
                        "print(f\"      Kept only transport-relevant fuel: lad_lag_1 (diesel)\")\n",
                        "plt.show()\n"
                    ]
                    print("✓ Updated feature importance cell")
        
        # Write the updated notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        
        print(f"\n✅ Successfully updated {notebook_path}")
        print("\nNext steps:")
        print("1. Open the notebook in Jupyter/VS Code")
        print("2. Run the updated cell to regenerate the figure")
        print("3. The new figure will show 22 features with correct percentages")
        return 0
        
    except FileNotFoundError:
        print(f"❌ Error: {notebook_path} not found!")
        print("Make sure you're running this script from the RESEARCH-Final-year directory")
        return 1
    except Exception as e:
        print(f"❌ Error updating notebook: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(update_notebook())
