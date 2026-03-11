import pandas as pd
from scipy import stats

# 1. Load your dataset
# Replace 'your_file.xlsx' with the actual path to your file
df = pd.read_excel('data/data.xlsx')

# 2. Define the columns you want to test
# We use list comprehension to quickly grab the v1 through v5 columns
other_columns = [
    'score_vrise', 'score_phq', 'score_gad', 'score_stai_t', 
    'positive_affect_start', 'negative_affect_start', 
    'positive_affect_end', 'negative_affect_end'
]

target_columns = other_columns

# 3. Perform the Shapiro-Wilk Test
results = []
for col in target_columns:
    if col in df.columns:
        # Dropping NaNs is crucial or the test will return NaN
        data = df[col].dropna()
        
        if len(data) >= 3:  # Shapiro-Wilk requires at least 3 data points
            stat, p_value = stats.shapiro(data)
            
            # A common alpha level is 0.05
            is_normal = "Yes" if p_value > 0.05 else "No"
            
            results.append({
                'Variable': col,
                'Statistic': round(stat, 4),
                'p-value': round(p_value, 4),
                'Normally Distributed?': is_normal
            })
    else:
        print(f"Warning: Column '{col}' not found in the Excel file.")

# 4. Display results
results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

# Optional: Save results to a CSV
# results_df.to_csv('normality_test_results.csv', index=False)