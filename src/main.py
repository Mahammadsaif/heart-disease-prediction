# Heart Disease Prediction API with Database
# File: src/main.py
# Now we save predictions to database!

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import psycopg2
from datetime import datetime

# Load trained model
model_data = joblib.load('../models/heart_disease_model.pkl')
model = model_data['model']
feature_names = model_data['feature_names']

# Database configuration (same as our setup)
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'Mypassword#007',
    'database': 'heart_disease_db'
}

# Create FastAPI app
app = FastAPI(title="Heart Disease Prediction API", version="1.0.0")

# Define input data structure
class PatientData(BaseModel):
    name: str = "Unknown Patient"  # Added patient name
    age: int
    sex: int # 0 = female, 1 = male
    cp: int # chest pain type (0-3)
    trestbps: int # resting blood pressure
    chol: int # cholesterol
    fbs: int # fasting blood sugar (0 or 1)
    restecg: int # resting ECG (0-2)
    thalach: int # max heart rate
    exang: int # exercise angina (0 or 1)
    oldpeak: float # ST depression
    slope: int # slope of peak exercise ST (0-2)
    ca: int # number of vessels colored (0-3)
    thal: int # thalassemia (1-3)

# Define response structure
class PredictionResponse(BaseModel):
    prediction_id: int  # Added database ID
    patient_name: str
    prediction: int
    probability_no_disease: float
    probability_disease: float
    risk_level: str
    model_used: str
    prediction_date: str

# Helper function to save prediction to database
def save_prediction_to_db(patient_data: dict, prediction_result: dict):
    """Save prediction to PostgreSQL database"""
    try:
        # Connect to database
        connection = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Insert prediction with all patient data
        insert_sql = """
        INSERT INTO predictions (
            patient_name, age, sex, prediction, 
            disease_probability, risk_level
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, prediction_date
        """
        
        cursor.execute(insert_sql, (
            patient_data['name'],
            patient_data['age'],
            patient_data['sex'],
            prediction_result['prediction'],
            prediction_result['probability_disease'],
            prediction_result['risk_level']
        ))
        
        # Get the ID and timestamp of inserted record
        result = cursor.fetchone()
        prediction_id = result[0]
        prediction_date = result[1]
        
        cursor.close()
        connection.close()
        
        return prediction_id, prediction_date
        
    except Exception as e:
        print(f"Database error: {e}")
        return None, None

# Helper function to get recent predictions
def get_recent_predictions(limit=10):
    """Get recent predictions from database"""
    try:
        connection = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        cursor = connection.cursor()
        
        select_sql = """
        SELECT id, patient_name, age, sex, prediction, 
               disease_probability, risk_level, prediction_date
        FROM predictions 
        ORDER BY prediction_date DESC 
        LIMIT %s
        """
        
        cursor.execute(select_sql, (limit,))
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return results
        
    except Exception as e:
        print(f"Database error: {e}")
        return []

@app.get("/")
def read_root():
    return {
        "message": "Heart Disease Prediction API with Database!",
        "model": model_data['model_name'],
        "accuracy": model_data['accuracy'],
        "features": "Predictions are now saved to database"
    }

@app.get("/health")
def health_check():
    # Check if database is working
    try:
        recent = get_recent_predictions(1)
        db_status = "connected"
        total_predictions = len(get_recent_predictions(1000))  # Quick count
    except:
        db_status = "disconnected"
        total_predictions = 0
        
    return {
        "status": "healthy",
        "database": db_status,
        "total_predictions_stored": total_predictions
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_heart_disease(patient: PatientData):
    # Convert input to DataFrame (same as before)
    patient_data = patient.dict()
    
    # Remove name for model prediction (model doesn't need it)
    model_input = {k: v for k, v in patient_data.items() if k != 'name'}
    patient_df = pd.DataFrame([model_input])
    
    # Make prediction
    prediction = model.predict(patient_df)[0]
    probabilities = model.predict_proba(patient_df)[0]
    
    # Determine risk level
    disease_prob = probabilities[1]
    if disease_prob >= 0.7:
        risk_level = "High Risk"
    elif disease_prob >= 0.4:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"
    
    # Prepare prediction result
    prediction_result = {
        'prediction': int(prediction),
        'probability_disease': float(probabilities[1]),
        'risk_level': risk_level
    }
    
    # Save to database
    prediction_id, prediction_date = save_prediction_to_db(patient_data, prediction_result)
    
    # Return response with database info
    return PredictionResponse(
        prediction_id=prediction_id if prediction_id else 0,
        patient_name=patient.name,
        prediction=int(prediction),
        probability_no_disease=float(probabilities[0]),
        probability_disease=float(probabilities[1]),
        risk_level=risk_level,
        model_used=model_data['model_name'],
        prediction_date=str(prediction_date) if prediction_date else str(datetime.now())
    )

@app.get("/recent-predictions")
def get_recent():
    """Get recent predictions from database"""
    predictions = get_recent_predictions(10)
    
    if not predictions:
        return {"message": "No predictions found"}
    
    formatted_predictions = []
    for pred in predictions:
        formatted_predictions.append({
            "id": pred[0],
            "patient_name": pred[1],
            "age": pred[2],
            "sex": "Male" if pred[3] == 1 else "Female",
            "prediction": "Disease" if pred[4] == 1 else "No Disease",
            "disease_probability": round(pred[5], 3),
            "risk_level": pred[6],
            "prediction_date": str(pred[7])
        })
    
    return {
        "total_predictions": len(formatted_predictions),
        "predictions": formatted_predictions
    }

@app.get("/stats")
def get_prediction_stats():
    """Get statistics about predictions"""
    try:
        predictions = get_recent_predictions(1000)  # Get more for stats
        
        if not predictions:
            return {"message": "No predictions available"}
        
        total_predictions = len(predictions)
        disease_count = sum(1 for pred in predictions if pred[4] == 1)
        no_disease_count = total_predictions - disease_count
        
        # Risk level stats
        high_risk = sum(1 for pred in predictions if pred[6] == "High Risk")
        medium_risk = sum(1 for pred in predictions if pred[6] == "Medium Risk")
        low_risk = sum(1 for pred in predictions if pred[6] == "Low Risk")
        
        return {
            "total_predictions": total_predictions,
            "disease_predictions": disease_count,
            "no_disease_predictions": no_disease_count,
            "disease_rate": round(disease_count/total_predictions*100, 1),
            "risk_distribution": {
                "high_risk": high_risk,
                "medium_risk": medium_risk,
                "low_risk": low_risk
            }
        }
    except Exception as e:
        return {"error": f"Could not get stats: {e}"}

@app.get("/model-info")
def get_model_info():
    return {
        "model_name": model_data['model_name'],
        "accuracy": model_data['accuracy'],
        "features": feature_names,
        "total_features": len(feature_names),
        "database_integration": "Active"
    }

# For testing locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)