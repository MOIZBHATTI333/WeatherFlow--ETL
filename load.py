# load.py
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:
    raise ValueError("DATABASE_URL not found in .env file")

def get_engine():
    return create_engine(DB_URL)

def create_tables():
    engine = get_engine()
    with engine.begin() as conn:
        # Create weather_data table (PostgreSQL compatible)
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
    print("Tables created or already exist.")

def load_weather_data(df: pd.DataFrame):
    engine = get_engine()
    # Insert into weather_data table
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO weather_data 
                    (location, temperature, windspeed, humidity, precipitation, weathercode, forecast_time)
                VALUES 
                    (:location, :temperature, :windspeed, :humidity, :precipitation, :weathercode, :forecast_time)
            """), {
                'location': row['city'],
                'temperature': row['temp_c'],
                'windspeed': row['wind_kph'],
                'humidity': row['humidity_pct'],
                'precipitation': row['precipitation'],
                'weathercode': row['weathercode'],
                'forecast_time': row['observed_at']  # PostgreSQL can handle datetime objects
            })
    print(f"Loaded {len(df)} rows to weather_data")

def refresh_summary():
    """Recalculate the daily summary from scratch."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE daily_weather_summary"))
        conn.execute(text("""
            INSERT INTO daily_weather_summary
                (date, city, avg_temp_c, max_temp_c, min_temp_c,
                 total_precip_mm, avg_humidity, avg_wind_kph, rainy_hours)
            SELECT
                date,
                city,
                ROUND(AVG(temp_c)::numeric, 2),
                MAX(temp_c),
                MIN(temp_c),
                SUM(precipitation),
                ROUND(AVG(humidity_pct)::numeric, 1),
                ROUND(AVG(wind_kph)::numeric, 2),
                COUNT(*) FILTER (WHERE is_raining)
            FROM raw_weather
            WHERE is_suspect = FALSE
            GROUP BY date, city
        """))
    print("Summary mart refreshed")