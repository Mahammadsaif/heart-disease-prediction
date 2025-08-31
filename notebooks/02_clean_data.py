import pandas as pd
import numpy as np

print("Cleaning Heart Disease Dataset")
print("=" * 40)

df = pd.read_csv('../data/heart_disease.csv')
print(f"Original data shape: {df.shape}")

print("\nConverting '?' to proper missing values")
df = df.replace('?', np.nan)
print("Converted all '?' to NaN")

print("\nConverting data types")
numeric_columns = ['ca', 'thal']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col])
    print(f"{col} converted to numeric")

print("\nHandling missing values")
for col in ['ca', 'thal']:
    if df[col].isnull().sum() > 0:
        median_value = df[col].median()
        df[col].fillna(median_value, inplace=True)
        print(f"Filled {col} missing values with median: {median_value}")

print("\nConverting target to binary")
df['target_binary'] = (df['target'] > 0).astype(int)
print(f"No disease (0): {sum(df['target_binary'] == 0)} patients")
print(f"Has disease (1): {sum(df['target_binary'] == 1)} patients")

df_clean = df.copy()
df_clean = df_clean.drop('target', axis=1)
df_clean = df_clean.rename(columns={'target_binary': 'target'})

df_clean.to_csv('../data/heart_disease_clean.csv', index=False)
print(f"\nCleaned data saved. Final shape: {df_clean.shape}")