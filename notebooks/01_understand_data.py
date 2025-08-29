import pandas as pd
import numpy as np

print(" Understanding Our Heart Disease Dataset")
print("=" * 50)

# Load the data we downloaded
df = pd.read_csv('../data/heart_disease.csv')

print(" BASIC INFO:")
print(f"Shape: {df.shape}")
print(f"Rows (patients): {df.shape[0]}")
print(f"Columns (features): {df.shape[1]}")

# Let's see what each column means (DOMAIN KNOWLEDGE - important for interviews!)
print("\n WHAT EACH FEATURE MEANS:")
feature_meanings = {
    'age': 'Age in years',
    'sex': 'Sex (1 = male, 0 = female)', 
    'cp': 'Chest pain type (0-3: typical angina, atypical, non-anginal, asymptomatic)',
    'trestbps': 'Resting blood pressure (mm Hg)',
    'chol': 'Serum cholesterol (mg/dl)',
    'fbs': 'Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)',
    'restecg': 'Resting ECG results (0-2: normal, ST-T abnormality, LV hypertrophy)',
    'thalach': 'Maximum heart rate achieved',
    'exang': 'Exercise induced angina (1 = yes, 0 = no)',
    'oldpeak': 'ST depression induced by exercise relative to rest',
    'slope': 'Slope of peak exercise ST segment (0-2: upsloping, flat, downsloping)',
    'ca': 'Number of major vessels colored by fluoroscopy (0-3)',
    'thal': 'Thalassemia (1 = normal, 2 = fixed defect, 3 = reversible defect)',
    'target': 'Heart disease (0 = no, 1-4 = severity levels)'
}

for col, meaning in feature_meanings.items():
    print(f"• {col:10}: {meaning}")

# Look at first few rows
print(f"\n FIRST 5 ROWS:")
print(df.head())

# Check data types - this is where we find problems!
print(f"\n DATA TYPES:")
print(df.dtypes)

# THE REAL WORLD PROBLEM: Missing values marked as '?'
print(f"\n MISSING VALUES (marked as '?'):")
for col in df.columns:
    question_marks = (df[col] == '?').sum() if df[col].dtype == 'object' else 0
    null_values = df[col].isnull().sum()
    total_missing = question_marks + null_values
    if total_missing > 0:
        print(f"• {col}: {total_missing} missing ({total_missing/len(df)*100:.1f}%)")

# Check unique values in each column to spot problems
print(f"\n UNIQUE VALUES PER COLUMN (spotting data issues):")
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"• {col:10}: {unique_count} unique values")
    
    # Show actual unique values for categorical-looking columns
    if unique_count < 10:
        print(f"            Values: {sorted(df[col].unique())}")

# Look at target distribution
print(f"\n TARGET DISTRIBUTION (what we want to predict):")
print(df['target'].value_counts().sort_index())

# This is messy! In medical data:
# 0 = no disease
# 1, 2, 3, 4 = different severity levels
# But most ML tutorials just make it binary (0 vs 1+)

print(f"\n DATA ISSUES WE NEED TO FIX:")
issues = []

# Check for '?' values
for col in df.columns:
    if df[col].dtype == 'object':
        if (df[col] == '?').sum() > 0:
            issues.append(f"• Column '{col}' has '?' instead of proper missing values")

# Check data types
for col in df.columns:
    if col != 'target' and df[col].dtype == 'object':
        issues.append(f"• Column '{col}' is stored as text but should be numeric")

# Check target
if len(df['target'].unique()) > 2:
    issues.append("• Target has multiple classes (0,1,2,3,4) - need to decide binary vs multiclass")

if len(issues) == 0:
    print(" No major issues found!")
else:
    for issue in issues:
        print(issue)

print(f"\n NEXT STEPS:")
print("1. Convert '?' to proper NaN values")
print("2. Convert text columns to numbers") 
print("3. Handle missing values properly")
print("4. Convert target to binary (disease vs no disease)")
print("5. Check for outliers and data quality issues")

print(f"\n Data understanding complete!")
print("This is the messy reality of real datasets!")