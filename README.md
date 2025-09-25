🫀 Heart Disease Prediction
    This project predicts the likelihood of heart disease using patient health data and a trained Random Forest model.

It includes:
    Frontend: Built with Next.js (React framework) for a clean UI.
    Backend: FastAPI serving the ML model and handling API requests.
    Database: PostgreSQL (with Docker) for structured storage of patient data.
    Machine Learning: Random Forest classifier trained on the UCI Heart Disease dataset.


📊 Workflow
    User enters health details in the Next.js frontend form.
    The form sends input to the FastAPI backend.
    Backend runs the trained Random Forest model on the input.
    Prediction (heart disease risk: Yes/No, with probability %) is returned.
    (Optional) Data can be saved in PostgreSQL for future reference.


⚙️ Tech Stack
    Frontend: Next.js (React, TailwindCSS)
    Backend: FastAPI (Python)
    Database: PostgreSQL (Dockerized)
    ML Model: Random Forest (scikit-learn)


🚀 Getting Started

1. Clone the Repo
    git clone https://github.com/Mahammadsaif/heart-disease-prediction.git
    cd heart-disease-prediction

2. Run with Docker Compose
    docker-compose up --build
    Frontend → http://localhost:3000
    Backend API → http://localhost:8000


📂 Project Structure
    heart-disease-prediction/
    │── backend/        # FastAPI + ML model
    │── frontend/       # Next.js UI
    │── notebooks/      # Data preprocessing, training
    │── docker-compose.yml
    │── Dockerfile
    │── requirements.txt
    │── README.md


📖 Example Input
    Feature	Example Value
    Age	45
    Sex	1 (Male)
    Cholesterol	210
    BP	130
    MaxHR	170

Output:
    Heart Disease Risk: 78% (Positive)


🎯 Why Random Forest?
    Handles both numerical & categorical features well.
    Robust against overfitting compared to a single decision tree.
    Provides feature importance (to explain model decisions).


🙌 Acknowledgements
    Dataset: UCI Heart Disease dataset
    Tools: scikit-learn, FastAPI, Next.js, PostgreSQL