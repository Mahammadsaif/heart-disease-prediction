import pandas as pd
import numpy as np

print("Understanding Our Heart Disease Dataset")
print("=" * 50)

df = pd.read_csv('../data/heart_disease.csv')
print(f"Shape: {df.shape}")
print(f"Rows (patients): {df.shape[0]}")
print(f"Columns (features): {df.shape[1]}")

print("\nWHAT EACH FEATURE MEANS:")
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

print(f"\nFIRST 5 ROWS:")
print(df.head())

print(f"\nDATA TYPES:")
print(df.dtypes)

print(f"\nMISSING VALUES (marked as '?'):")
for col in df.columns:
    question_marks = (df[col] == '?').sum() if df[col].dtype == 'object' else 0
    null_values = df[col].isnull().sum()
    total_missing = question_marks + null_values
    if total_missing > 0:
        print(f"• {col}: {total_missing} missing ({total_missing/len(df)*100:.1f}%)")

print(f"\nUNIQUE VALUES PER COLUMN:")
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"• {col:10}: {unique_count} unique values")
    if unique_count < 10:
        print(f"  Values: {sorted(df[col].unique())}")

print(f"\nTARGET DISTRIBUTION:")
print(df['target'].value_counts().sort_index())