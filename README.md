# Weather ETL Pipeline

This project extracts weather forecast data from the Open-Meteo API, transforms it, and loads it into a PostgreSQL database for use in Power BI dashboards.

## Features

- Extracts hourly weather data for 6 Pakistani cities
- Stores data in `weather_data` table with real-time timestamps
- Automatic data refresh every 30 minutes
- PostgreSQL database support

## Setup

### 1. Install PostgreSQL
Download and install PostgreSQL from https://www.postgresql.org/download/

### 2. Create Environment File
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 3. Install Dependencies
```bash
pip install requests pandas sqlalchemy psycopg2-binary python-dotenv schedule
```

### 4. Setup Database
```bash
python setup_postgres.py
```

### 5. Run the Pipeline
```bash
python run_pipeline.py
```

## Automated Refresh

To keep your Power BI dashboard updated with fresh data:

### Option 1: Run Scheduler Script
```bash
python scheduler.py
```
This will run continuously, refreshing data every 30 minutes.

### Option 2: Windows Background Process
Double-click `run_scheduler.bat` to run the scheduler in the background without a console window.

### Option 3: Windows Task Scheduler
1. Open Task Scheduler
2. Create a new task
3. Set trigger to run every 30 minutes
4. Action: Start a program -> `python.exe`
5. Arguments: `run_pipeline.py`
6. Start in: `f:\weather-etl-pipeline`

## Database

- **Type**: PostgreSQL
- **Table**: `weather_data`
- **Columns**: id, fetched_at, location, temperature, windspeed, humidity, precipitation, weathercode, forecast_time


## Environment Variables

Create a `.env` file with:
```
DATABASE_URL=postgresql://username:password@host:port/database
# OR individual variables:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weather_db
DB_USER=postgres
DB_PASSWORD=your_password
```