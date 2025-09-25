from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import pg8000.native
from datetime import datetime
from typing import Any, List, Tuple, Optional
import os
import joblib

model_path = os.path.join(os.path.dirname(__file__), "..", "models", "heart_disease_model.pkl")
model_obj = joblib.load(model_path)

if hasattr(model_obj, "predict"):
    model = model_obj
    feature_names = getattr(model_obj, "feature_names", None)
    model_name = getattr(model_obj, "model_name", "model")
    model_accuracy = getattr(model_obj, "accuracy", None)
else:
    model_data = model_obj if isinstance(model_obj, dict) else {}
    model = model_data.get("model")
    feature_names = model_data.get("feature_names") or model_data.get("features")
    model_name = model_data.get("model_name", "model")
    model_accuracy = model_data.get("accuracy")

if feature_names is None:
    feature_names = [
        "age","sex","cp","trestbps","chol","fbs","restecg",
        "thalach","exang","oldpeak","slope","ca","thal"
    ]

if model is None:
    raise RuntimeError("Could not find trained model in models/heart_disease_model.pkl")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "database": os.getenv("DB_NAME", "heart_disease"),
}

app = FastAPI(title="Heart Disease Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    name: str = "Unknown Patient"
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

class PredictionResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    prediction_id: int
    patient_name: str
    prediction: int
    probability_no_disease: float
    probability_disease: float
    risk_level: str
    model_used: str
    prediction_date: str

def get_db_connection() -> pg8000.native.Connection:
    return pg8000.native.Connection(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
    )

@app.on_event("startup")
def create_table_if_not_exists():
    try:
        conn = get_db_connection()
        conn.run("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            patient_name TEXT,
            age INT,
            sex INT,
            cp INT,
            trestbps INT,
            chol INT,
            fbs INT,
            restecg INT,
            thalach INT,
            exang INT,
            oldpeak FLOAT,
            slope INT,
            ca INT,
            thal INT,
            prediction INT,
            disease_probability FLOAT,
            risk_level TEXT,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.run("COMMIT")
        conn.close()
    except Exception as e:
        print("DB Table Error:", e)


def save_prediction_to_db(patient: dict, prediction_result: dict) -> Tuple[Optional[int], Optional[str]]:
    try:
        conn = get_db_connection()
        sql = """
        INSERT INTO predictions (
            patient_name, age, sex, cp, trestbps, chol, fbs, restecg,
            thalach, exang, oldpeak, slope, ca, thal,
            prediction, disease_probability, risk_level
        )
        VALUES (
            :name, :age, :sex, :cp, :trestbps, :chol, :fbs, :restecg,
            :thalach, :exang, :oldpeak, :slope, :ca, :thal,
            :prediction, :prob, :risk
        )
        RETURNING id, prediction_date
        """
        result = conn.run(
            sql,
            name=patient["name"],
            age=patient["age"],
            sex=patient["sex"],
            cp=patient["cp"],
            trestbps=patient["trestbps"],
            chol=patient["chol"],
            fbs=patient["fbs"],
            restecg=patient["restecg"],
            thalach=patient["thalach"],
            exang=patient["exang"],
            oldpeak=patient["oldpeak"],
            slope=patient["slope"],
            ca=patient["ca"],
            thal=patient["thal"],
            prediction=prediction_result["prediction"],
            prob=prediction_result["probability_disease"],
            risk=prediction_result["risk_level"],
        )
        conn.run("COMMIT")
        conn.close()
        if not result:
            return None, None
        row = result[0]
        return int(row[0]), str(row[1])
    except Exception as e:
        print("DB Insert Error:", e)
        return None, None


def fetch_recent(limit: int = 10) -> List[tuple]:
    try:
        conn = get_db_connection()
        limit = max(1, int(limit))
        sql = f"""
        SELECT id, patient_name, age, sex, prediction, disease_probability, risk_level, prediction_date
        FROM predictions
        ORDER BY prediction_date DESC
        LIMIT {limit}
        """
        rows = conn.run(sql)
        conn.close()
        return rows or []
    except:
        return []

@app.get("/")
def root():
    return {"message": "Heart Disease Prediction API with Database", "model": model_name, "accuracy": model_accuracy}

@app.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientData):
    patient_dict = patient.dict()
    row = [[patient_dict.get(fn) for fn in feature_names]]
    df = pd.DataFrame(row, columns=feature_names)
    pred = int(model.predict(df)[0])
    probs = model.predict_proba(df)[0]
    prob_no = float(probs[0])
    prob_yes = float(probs[1])
    threshold = 0.4
    pred = 1 if prob_yes >= threshold else 0
    if prob_yes >= 0.7:
        risk = "High Risk"
    elif prob_yes >= threshold:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"
    prediction_result = {"prediction": pred, "probability_disease": prob_yes, "risk_level": risk}
    pred_id, pred_date = save_prediction_to_db(patient_dict, prediction_result)
    return PredictionResponse(
        prediction_id=pred_id if pred_id else 0,
        patient_name=patient_dict.get("name", "Unknown"),
        prediction=pred,
        probability_no_disease=prob_no,
        probability_disease=prob_yes,
        risk_level=risk,
        model_used=model_name,
        prediction_date=pred_date if pred_date else str(datetime.now()),
    )

@app.get("/recent-predictions")
def recent_predictions():
    rows = fetch_recent(10)
    preds = []
    for r in rows:
        preds.append({
            "id": int(r[0]),
            "patient_name": r[1],
            "age": int(r[2]) if r[2] is not None else None,
            "sex": "Male" if r[3] == 1 else "Female",
            "prediction": "Disease" if r[4] == 1 else "No Disease",
            "disease_probability": round(float(r[5]) if r[5] is not None else 0.0, 3),
            "risk_level": r[6],
            "prediction_date": str(r[7]),
        })
    return {"total_predictions": len(preds), "predictions": preds}

@app.get("/stats")
def stats():
    rows = fetch_recent(1000)
    total = len(rows)
    if total == 0:
        return {"total_predictions": 0, "disease_predictions": 0, "no_disease_predictions": 0, "disease_rate": 0.0, "risk_distribution": {"high_risk": 0, "medium_risk": 0, "low_risk": 0}}
    disease_count = sum(1 for r in rows if r[4] == 1)
    no_disease_count = total - disease_count
    high_risk = sum(1 for r in rows if r[6] == "High Risk")
    medium_risk = sum(1 for r in rows if r[6] == "Medium Risk")
    low_risk = sum(1 for r in rows if r[6] == "Low Risk")
    return {"total_predictions": total, "disease_predictions": disease_count, "no_disease_predictions": no_disease_count, "disease_rate": round(disease_count / total * 100, 1), "risk_distribution": {"high_risk": high_risk, "medium_risk": medium_risk, "low_risk": low_risk}}
