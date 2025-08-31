# Heart Disease Prediction System

A full-stack machine learning application that predicts heart disease risk using patient medical data. Built with FastAPI, Next.js, and PostgreSQL.

## Features

- **ML-Powered Predictions**: Random Forest model with 85% accuracy
- **Complete Medical Assessment**: 13 clinical parameters for comprehensive analysis
- **Real-time Dashboard**: Analytics and prediction history
- **Database Storage**: PostgreSQL for persistent data management
- **Modern Frontend**: Responsive React/Next.js interface
- **RESTful API**: FastAPI backend with automatic documentation

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Robust relational database
- **scikit-learn** - Machine learning model training
- **Pandas** - Data processing and analysis

### Frontend
- **Next.js 14** - React framework with TypeScript
- **Tailwind CSS** - Utility-first styling
- **Server-side rendering** - Optimized performance

## Project Structure

```
heart_disease_project/
├── data/                   # Dataset files
├── models/                 # Trained ML models
├── notebooks/              # Data analysis and model training
│   ├── 01_understand_data.py
│   ├── 02_clean_data.py
│   ├── 03_build_model.py
│   └── 04_add_database.py
├── src/                    # Backend API
│   └── main.py
└── frontend/               # Next.js application
    └── src/app/
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pandas scikit-learn joblib psycopg2-binary

# Start PostgreSQL and create database
psql -U postgres
CREATE DATABASE heart_disease_db;

# Run database setup
cd notebooks
python 04_add_database.py

# Start API server
cd ../src
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. **Access the application**: http://localhost:3000
2. **Enter patient data**: Complete all 13 medical parameters
3. **Get prediction**: AI model provides risk assessment
4. **View dashboard**: Analyze prediction trends and statistics

## API Endpoints

- `GET /` - API information
- `POST /predict` - Make heart disease prediction
- `GET /recent-predictions` - Retrieve prediction history
- `GET /stats` - Get prediction statistics
- `GET /health` - System health check

## Model Performance

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 85%
- **Features**: 13 clinical parameters
- **Validation**: Stratified train-test split

## Medical Parameters

The model analyzes these clinical indicators:
- Age, sex, chest pain type
- Blood pressure and cholesterol levels
- ECG results and heart rate data
- Exercise stress test results
- Cardiac imaging parameters

## Contributing

This project was built for educational purposes to demonstrate:
- End-to-end ML pipeline development
- Full-stack web application architecture
- Database integration and API design
- Modern frontend development practices

## Deployment

- **Backend**: Deployed on Render
- **Frontend**: Deployed on Vercel
- **Database**: PostgreSQL on Render

## License

This project is for educational and portfolio purposes.

## Author

**Saif Shaik**
- LinkedIn: https://www.linkedin.com/in/saif-shaik/

---

*This application is for educational demonstration only and should not be used for actual medical diagnosis.*