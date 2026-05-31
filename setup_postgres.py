# setup_postgres.py
import os
from sqlalchemy import create_engine, text

# PostgreSQL connection details
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "weather_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "221334")

def create_database():
    """Create the weather_db database if it doesn't exist."""
    # Connect to default postgres database to create our database
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres")

    with engine.begin() as conn:
        # Create database if it doesn't exist
        conn.execute(text("COMMIT"))  # Required for CREATE DATABASE
        try:
            conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"Database '{DB_NAME}' created successfully.")
        except Exception as e:
            if "already exists" in str(e):
                print(f"Database '{DB_NAME}' already exists.")
            else:
                raise e

def create_tables():
    """Create the weather_data table."""
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id            SERIAL PRIMARY KEY,
                fetched_at    TIMESTAMP DEFAULT NOW(),
                location      VARCHAR(100),
                temperature   FLOAT,
                windspeed     FLOAT,
                humidity      FLOAT,
                precipitation FLOAT,
                weathercode   INTEGER,
                forecast_time TIMESTAMP
            )
        """))
    print("Tables created successfully.")

def main():
    print("Setting up PostgreSQL database...")
    create_database()
    create_tables()
    print("PostgreSQL setup complete!")

if __name__ == "__main__":
    main()