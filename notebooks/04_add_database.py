# Step 4: Adding Simple Database to Store Predictions
# File: notebooks/04_add_database.py
# Let's learn databases step by step!

import psycopg2
import pandas as pd
from datetime import datetime

print("🗄️ Learning Database with Heart Disease Project")
print("=" * 50)

# STEP 1: Connect to PostgreSQL
# This is like opening the database door
print("\n🔧 STEP 1: Connecting to PostgreSQL")

# Database info - like your address
DB_HOST = "localhost"      # Database is on your computer
DB_PORT = "5432"          # PostgreSQL default port
DB_USER = "postgres"      # Username
DB_PASSWORD = "Mypassword#007"  # Your password
DB_NAME = "heart_disease_db"    # Our database name

# Try to connect
try:
    # First connect to 'postgres' database (always exists)
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database="postgres"  # Connect to default database first
    )
    connection.autocommit = True  # Auto-save changes
    cursor = connection.cursor()
    print("✅ Connected to PostgreSQL!")
    
except Exception as error:
    print(f"❌ Can't connect to PostgreSQL: {error}")
    print("Make sure PostgreSQL is running!")
    exit()

# STEP 2: Create our database
print("\n🔧 STEP 2: Creating our database")

# Check if database exists
cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'heart_disease_db'")
database_exists = cursor.fetchone()

if database_exists:
    print("✅ Database 'heart_disease_db' already exists")
else:
    # Create new database
    cursor.execute("CREATE DATABASE heart_disease_db")
    print("✅ Created database 'heart_disease_db'")

# Close connection to postgres database
cursor.close()
connection.close()

# STEP 3: Connect to OUR database
print("\n🔧 STEP 3: Connecting to our heart disease database")

try:
    # Now connect to our new database
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME  # Connect to OUR database
    )
    connection.autocommit = True
    cursor = connection.cursor()
    print("✅ Connected to our heart_disease_db!")
    
except Exception as error:
    print(f"❌ Can't connect to heart_disease_db: {error}")
    exit()

# STEP 4: Create table to store predictions
print("\n🔧 STEP 4: Creating table to store predictions")

# SQL to create table - like creating a spreadsheet structure
create_table_sql = """
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(100),
    age INTEGER,
    sex INTEGER,
    prediction INTEGER,
    disease_probability FLOAT,
    risk_level VARCHAR(20),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# Execute the SQL
cursor.execute(create_table_sql)
print("✅ Created 'predictions' table")

# STEP 5: Insert a test prediction
print("\n🔧 STEP 5: Adding a test prediction")

# Sample prediction data
test_prediction = {
    'patient_name': 'Test Patient',
    'age': 45,
    'sex': 1,  # 1 = male
    'prediction': 1,  # 1 = has disease
    'disease_probability': 0.75,
    'risk_level': 'High Risk'
}

# SQL to insert data
insert_sql = """
INSERT INTO predictions (patient_name, age, sex, prediction, disease_probability, risk_level)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# Insert the data
cursor.execute(insert_sql, (
    test_prediction['patient_name'],
    test_prediction['age'],
    test_prediction['sex'],
    test_prediction['prediction'],
    test_prediction['disease_probability'],
    test_prediction['risk_level']
))

print("✅ Inserted test prediction")

# STEP 6: Read data back (to verify it worked)
print("\n🔧 STEP 6: Reading our data back")

# Select all predictions
cursor.execute("SELECT * FROM predictions")
all_predictions = cursor.fetchall()

print(f"Found {len(all_predictions)} predictions:")
for row in all_predictions:
    print(f"• ID: {row[0]}, Patient: {row[1]}, Age: {row[2]}, Risk: {row[6]}")

# STEP 7: Create simple functions for our API to use
print("\n🔧 STEP 7: Creating helper functions")

def save_prediction_to_db(patient_data, prediction_result):
    """
    Simple function to save prediction to database
    
    patient_data: dict with patient info
    prediction_result: dict with prediction results
    """
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER, 
            password=DB_PASSWORD, database=DB_NAME
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Insert prediction
        insert_sql = """
        INSERT INTO predictions (patient_name, age, sex, prediction, disease_probability, risk_level)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        cur.execute(insert_sql, (
            patient_data.get('name', 'Unknown'),
            patient_data['age'],
            patient_data['sex'],
            prediction_result['prediction'],
            prediction_result['probability_disease'],
            prediction_result['risk_level']
        ))
        
        # Get the ID of inserted record
        prediction_id = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return prediction_id
        
    except Exception as e:
        print(f"Error saving to database: {e}")
        return None

def get_recent_predictions(limit=5):
    """Get recent predictions from database"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER, 
            password=DB_PASSWORD, database=DB_NAME
        )
        cur = conn.cursor()
        
        # Get recent predictions
        select_sql = """
        SELECT patient_name, age, sex, prediction, risk_level, prediction_date
        FROM predictions 
        ORDER BY prediction_date DESC 
        LIMIT %s
        """
        
        cur.execute(select_sql, (limit,))
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return results
        
    except Exception as e:
        print(f"Error reading from database: {e}")
        return []

# Test our functions
print("Testing our helper functions:")

# Test data
test_patient = {'name': 'John Doe', 'age': 55, 'sex': 1}
test_result = {
    'prediction': 0,
    'probability_disease': 0.3,
    'risk_level': 'Low Risk'
}

# Save test prediction
saved_id = save_prediction_to_db(test_patient, test_result)
if saved_id:
    print(f"✅ Saved prediction with ID: {saved_id}")

# Get recent predictions
recent = get_recent_predictions(3)
print(f"\nRecent predictions:")
for pred in recent:
    print(f"• {pred[0]}: Age {pred[1]}, Risk {pred[4]}")

# Clean up
cursor.close()
connection.close()

print("\n🎯 WHAT YOU LEARNED:")
print("• How to connect to PostgreSQL from Python")
print("• How to create databases and tables with SQL")
print("• How to INSERT data into database")
print("• How to SELECT data from database")
print("• How to write helper functions for database operations")
print("• Error handling with try/except blocks")

print(f"\n✅ Database setup complete!")
print("Next: Update your FastAPI to save predictions")

# Save database connection info for other files
db_config = {
    'host': DB_HOST,
    'port': DB_PORT,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME
}

print(f"\n💾 Database config saved for main.py to use")