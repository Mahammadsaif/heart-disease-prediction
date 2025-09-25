🫀 Heart Disease Prediction App

📌 Overview
A full-stack Machine Learning application that predicts the risk of heart disease based on medical data.
Built with FastAPI, Next.js, PostgreSQL, and Docker, the app provides real-time predictions using a trained Random Forest model and stores patient results in a database.
🚀 Live Demo
Frontend (Vercel) → Coming soon
Backend API (Render) → Coming soon

✨ Features
✅ Predict heart disease risk (Low / Medium / High).
✅ REST API built with FastAPI.
✅ Random Forest ML model trained on UCI Heart Disease dataset.
✅ Database integration (PostgreSQL) for storing past predictions.
✅ Frontend built with Next.js for user interaction.
✅ Fully containerized with Docker + Docker Compose.
✅ Ready for cloud deployment (Render, Vercel, AWS).

🛠 Tech Stack
Frontend: Next.js, React, TailwindCSS
Backend: FastAPI, Python
ML Model: Random Forest (scikit-learn, joblib)
Database: PostgreSQL
Containerization: Docker, Docker Compose
Deployment: Render (Backend), Vercel (Frontend)

⚙️ Workflow
User enters patient details (age, cholesterol, BP, etc.).
Frontend (Next.js) sends request → Backend (FastAPI API).
Backend loads trained Random Forest model.
Model predicts probability of heart disease.
Result + probability + risk level are stored in PostgreSQL DB.
User sees prediction on frontend with clean UI.

🧑‍⚕️ Input Features Explained
Age → Age of patient
Sex → Male (1) / Female (0)
cp (Chest Pain Type) → 0: Typical Angina, 1: Atypical Angina, 2: Non-anginal, 3: Asymptomatic
trestbps → Resting blood pressure (mm Hg)
chol → Serum cholesterol (mg/dl)
fbs → Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)
restecg → Resting ECG results (0–2)
thalach → Maximum heart rate achieved
exang → Exercise induced angina (1 = yes, 0 = no)
oldpeak → ST depression induced by exercise
slope → Slope of peak exercise ST segment (0–2)
ca → Number of major vessels colored by fluoroscopy (0–3)
thal → 0: Normal, 1: Fixed defect, 2: Reversible defect

📊 Example API Call
curl -X POST http://localhost:8000/predict \
-H "Content-Type: application/json" \
-d '{
  "name":"John Doe",
  "age":45,"sex":1,"cp":0,"trestbps":130,"chol":210,
  "fbs":0,"restecg":0,"thalach":170,"exang":0,"oldpeak":0.5,
  "slope":1,"ca":0,"thal":2
}'

Response:
{
  "prediction_id": 1,
  "patient_name": "John Doe",
  "prediction": 0,
  "probability_no_disease": 0.93,
  "probability_disease": 0.07,
  "risk_level": "Low Risk",
  "model_used": "Random Forest",
  "prediction_date": "2025-09-25 18:53:25"
}

🚀 Getting Started (Local Setup)
1️⃣ Clone Repository
git clone https://github.com/Mahammadsaif/heart-disease-prediction.git
cd heart-disease-prediction
2️⃣ Run with Docker
docker-compose up --build
Backend → http://localhost:8000
Frontend → http://localhost:3000
3️⃣ Check API
curl http://localhost:8000/

📂 Project Structure
heart-disease-prediction/
│── src/                # Backend (FastAPI + ML Model)
│   ├── main.py         # API routes & logic
│   ├── model.pkl       # Trained Random Forest model
│── frontend/           # Frontend (Next.js)
│── Dockerfile          # Backend Docker setup
│── docker-compose.yml  # Multi-container setup
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation

📈 Future Improvements
🔹 Add more ML models (XGBoost, Neural Networks).
🔹 Authentication for patient history.
🔹 Deploy on AWS/GCP for production scale.
🔹 CI/CD pipeline integration.

👨‍💻 Author
Shaik Saif
GitHub: Mahammadsaif
LinkedIn: (https://www.linkedin.com/in/saif-shaik/)
