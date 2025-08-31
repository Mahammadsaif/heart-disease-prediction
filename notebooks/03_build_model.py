import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

df = pd.read_csv('../data/heart_disease_clean.csv')
print(f"Data loaded: {df.shape}")
print(f"Target distribution:\n{df['target'].value_counts()}")

X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

print("Training models...")
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_train, y_train)

rf_pred = rf.predict(X_test)
lr_pred = lr.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)
lr_accuracy = accuracy_score(y_test, lr_pred)

print(f"Random Forest Accuracy: {rf_accuracy:.3f}")
print(f"Logistic Regression Accuracy: {lr_accuracy:.3f}")

if rf_accuracy > lr_accuracy:
    best_model = rf
    best_pred = rf_pred
    model_name = "Random Forest"
    best_accuracy = rf_accuracy
else:
    best_model = lr
    best_pred = lr_pred
    model_name = "Logistic Regression"
    best_accuracy = lr_accuracy

print(f"Best model: {model_name} with {best_accuracy:.3f} accuracy")

print("\nClassification Report:")
print(classification_report(y_test, best_pred))

if model_name == "Random Forest":
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nTop 5 Important Features:")
    print(feature_importance.head())

model_data = {
    'model': best_model,
    'feature_names': list(X.columns),
    'model_name': model_name,
    'accuracy': best_accuracy
}

joblib.dump(model_data, '../models/heart_disease_model.pkl')
print(f"\nModel saved to ../models/heart_disease_model.pkl")