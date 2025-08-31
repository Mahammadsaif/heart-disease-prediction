import psycopg2

print("Setting up PostgreSQL Database")
print("=" * 40)

DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'Mypassword#007',
    'database': 'heart_disease_db'
}

try:
    connection = psycopg2.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database="postgres"
    )
    connection.autocommit = True
    cursor = connection.cursor()
    print("Connected to PostgreSQL")
    
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'heart_disease_db'")
    if not cursor.fetchone():
        cursor.execute("CREATE DATABASE heart_disease_db")
        print("Created heart_disease_db database")
    
    cursor.close()
    connection.close()
    
    connection = psycopg2.connect(**DB_CONFIG)
    connection.autocommit = True
    cursor = connection.cursor()
    
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
    
    cursor.execute(create_table_sql)
    print("Created predictions table")
    
    cursor.close()
    connection.close()
    print("Database setup complete")
    
except Exception as error:
    print(f"Database error: {error}")