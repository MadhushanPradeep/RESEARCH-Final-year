#!/usr/bin/env python3
import json
import sys

# Read the notebook
with open('Multivariate_LSTM_V2 .ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

fixed = False

# Find Cell 62 and fix the X_test_sample issue
for cell_idx, cell in enumerate(nb['cells']):
    if 'source' in cell and isinstance(cell['source'], list):
        # Check if this is Cell 62
        for line in cell['source']:
            if 'CELL 62: SHAP Visualization' in line:
                print(f"Found Cell 62 at index {cell_idx}")
                
                # Find the line with "# Get feature values for the test sample"
                for i, source_line in enumerate(cell['source']):
                    if '# Get feature values for the test sample' in source_line:
                        print(f"Found target line at index {i}: {source_line[:50]}")
                        
                        # Create new defensive code
                        new_lines = [
                            "# Defensive: Check if X_test_sample exists from Cell 61\n",
                            "try:\n",
                            "    # Get feature values from Cell 61's sample\n",
                            "    X_test_sample_last = X_test_sample[:, -1, :]  # Last timestep\n",
                            "except NameError:\n",
                            "    # If Cell 61 not run, create sample from X_test\n",
                            "    print(\"⚠️  Warning: X_test_sample not found. Run Cell 61 first for consistent results.\")\n",
                            "    print(\"   Creating new sample from X_test for SHAP visualization...\")\n",
                            "    np.random.seed(42)\n",
                            "    test_sample_indices = np.random.choice(len(X_test), size=min(200, len(X_test)), replace=False)\n",
                            "    X_test_sample = X_test[test_sample_indices]\n",
                            "    X_test_sample_last = X_test_sample[:, -1, :]  # Last timestep\n",
                            "\n"
                        ]
                        
                        # Replace the old code (remove 2 lines: comment + X_test_sample_last =)
                        cell['source'] = cell['source'][:i] + new_lines + cell['source'][i+2:]
                        fixed = True
                        print(f"✅ Replaced {2} lines with {len(new_lines)} new lines")
                        break
                
                if fixed:
                    break
        if fixed:
            break

if fixed:
    # Write back the notebook
    with open('Multivariate_LSTM_V2 .ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print("✅ Notebook updated successfully!")
    print("✅ Cell 62 now has defensive check for X_test_sample variable")
else:
    print("❌ Could not find the target code to replace")
    sys.exit(1)
