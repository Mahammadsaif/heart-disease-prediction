import pg8000.native

print("Setting up PostgreSQL Database")
print("=" * 40)

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'Mypassword#007',
    'database': 'heart_disease_db'
}

try:
    # Connect to postgres database to create our database
    conn = pg8000.native.Connection(
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        database="postgres"
    )
    
    print("Connected to PostgreSQL")
    
    # Check if database exists
    result = conn.run("SELECT 1 FROM pg_database WHERE datname = :dbname", dbname=DB_CONFIG['database'])
    if not result:
        conn.run(f"CREATE DATABASE {DB_CONFIG['database']}")
        print("Created heart_disease_db database")
    
    conn.close()
    
    # Connect to our database
    conn = pg8000.native.Connection(**DB_CONFIG)
    
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
    
    conn.run(create_table_sql)
    print("Created predictions table")
    
    conn.close()
    print("Database setup complete")
    
except Exception as error:
    print(f"Database error: {error}")