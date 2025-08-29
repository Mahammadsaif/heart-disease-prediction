# Step 2: Cleaning Our Heart Disease Data
# File: notebooks/02_clean_data.py
# Let's fix the mess step by step!

import pandas as pd
import numpy as np

print("🧹 Cleaning Heart Disease Dataset")
print("=" * 40)

# Load our messy data
df = pd.read_csv('/Users/saifshaik/Desktop/heart_disease_project/data/heart_disease.csv')
print(f"Original data shape: {df.shape}")

# STEP 1: Fix the '?' problem
print(f"\n🔧 STEP 1: Converting '?' to proper missing values")

# Before fixing - let's see the problem
print("Before cleaning:")
for col in df.columns:
    if df[col].dtype == 'object':  # Only check text columns
        question_count = (df[col] == '?').sum()
        if question_count > 0:
            print(f"• {col}: {question_count} '?' values")

# Replace all '?' with NaN (Not a Number - proper missing value)
df = df.replace('?', np.nan)
print("✅ Converted all '?' to NaN")

# STEP 2: Convert columns to correct data types
print(f"\n🔧 STEP 2: Converting data types")

# These columns should be numeric but pandas read them as text
numeric_columns = ['ca', 'thal']  # These had '?' values so pandas made them 'object'

for col in numeric_columns:
    print(f"Converting {col} from {df[col].dtype} to numeric...")
    df[col] = pd.to_numeric(df[col])  # Convert text to numbers
    print(f"✅ {col} is now {df[col].dtype}")

# STEP 3: Check our missing values now
print(f"\n🔧 STEP 3: Checking missing values after conversion")
missing_values = df.isnull().sum()
print("Missing values per column:")
for col, count in missing_values.items():
    if count > 0:
        percentage = (count / len(df)) * 100
        print(f"• {col}: {count} missing ({percentage:.1f}%)")

# STEP 4: Handle missing values
print(f"\n🔧 STEP 4: Handling missing values")

# Strategy: Use median for numeric columns (robust to outliers)
for col in ['ca', 'thal']:
    if df[col].isnull().sum() > 0:
        median_value = df[col].median()
        print(f"Filling {col} missing values with median: {median_value}")
        df[col].fillna(median_value, inplace=True)
        print(f"✅ {col} - no more missing values")

# STEP 5: Convert target to binary
print(f"\n🔧 STEP 5: Converting target to binary")
print("Original target distribution:")
print(df['target'].value_counts().sort_index())

# In medical data: 0 = no disease, 1-4 = different severity levels
# For ML: we'll make it binary (0 = no disease, 1 = has disease)
df['target_binary'] = (df['target'] > 0).astype(int)

print("\nNew binary target distribution:")
print(df['target_binary'].value_counts())
print(f"• No disease (0): {sum(df['target_binary'] == 0)} patients")
print(f"• Has disease (1): {sum(df['target_binary'] == 1)} patients")

# STEP 6: Final data quality check
print(f"\n🔧 STEP 6: Final quality check")

# Check data types
print("Final data types:")
print(df.dtypes)

# Check for any remaining missing values
total_missing = df.isnull().sum().sum()
print(f"\nTotal missing values: {total_missing}")

if total_missing == 0:
    print("✅ No missing values left!")
else:
    print("❌ Still have missing values - need more cleaning")

# Check value ranges (spot outliers)
print(f"\nValue ranges (looking for outliers):")
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    min_val = df[col].min()
    max_val = df[col].max()
    mean_val = df[col].mean()
    print(f"• {col:12}: {min_val:6.1f} to {max_val:6.1f} (avg: {mean_val:6.1f})")

# STEP 7: Save cleaned data
print(f"\n💾 STEP 7: Saving cleaned data")

# Create clean dataset for modeling
df_clean = df.copy()

# Drop original target (keep binary version)
df_clean = df_clean.drop('target', axis=1)
df_clean = df_clean.rename(columns={'target_binary': 'target'})

# Save cleaned data
df_clean.to_csv('../data/heart_disease_clean.csv', index=False)
print(f"✅ Cleaned data saved to: ../data/heart_disease_clean.csv")
print(f"Final shape: {df_clean.shape}")

# STEP 8: Summary of what we fixed
print(f"\n📋 CLEANING SUMMARY:")
print("✅ Converted '?' to proper NaN values")
print("✅ Fixed data types (text → numeric)")
print("✅ Handled missing values with median")
print("✅ Converted target to binary classification")
print("✅ Verified no missing values remain")
print("✅ Saved clean dataset for modeling")

print(f"\n🎯 WHAT YOU LEARNED:")
print("• Real data is messy - need systematic cleaning")
print("• '?' vs NaN vs null - different types of missing data")
print("• Data types matter - text vs numeric affects models")
print("• Missing value strategies - median, mean, mode, or drop")
print("• Binary vs multiclass classification decisions")

print(f"\n✅ Data is now ready for modeling!")