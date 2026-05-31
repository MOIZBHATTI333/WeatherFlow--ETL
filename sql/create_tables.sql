-- sql/create_tables.sql

-- Layer 1: every raw row, untouched
CREATE TABLE IF NOT EXISTS raw_weather (
    id            SERIAL PRIMARY KEY,
    city          VARCHAR(50)  NOT NULL,
    observed_at   TIMESTAMP    NOT NULL,
    date          DATE         NOT NULL,
    hour          SMALLINT     NOT NULL,
    temp_c        NUMERIC(5,2),
    temp_f        NUMERIC(5,2),
    precipitation NUMERIC(6,2),
    wind_kph      NUMERIC(5,2),
    humidity_pct  SMALLINT,
    is_raining    BOOLEAN,
    is_suspect    BOOLEAN      DEFAULT FALSE,
    loaded_at     TIMESTAMP    DEFAULT NOW(),
    UNIQUE(city, observed_at)   -- prevent duplicate loads
);

-- Layer 2: daily summary mart (what Power BI / Looker reads)
CREATE TABLE IF NOT EXISTS daily_weather_summary (
    id              SERIAL PRIMARY KEY,
    date            DATE        NOT NULL,
    city            VARCHAR(50) NOT NULL,
    avg_temp_c      NUMERIC(5,2),
    max_temp_c      NUMERIC(5,2),
    min_temp_c      NUMERIC(5,2),
    total_precip_mm NUMERIC(6,2),
    avg_humidity    NUMERIC(5,1),
    avg_wind_kph    NUMERIC(5,2),
    rainy_hours     SMALLINT,
    updated_at      TIMESTAMP   DEFAULT NOW(),
    UNIQUE(date, city)
);

-- Weather data table as requested
CREATE TABLE IF NOT EXISTS weather_data (
    id            SERIAL PRIMARY KEY,
    fetched_at    TIMESTAMP DEFAULT NOW(),
    location      VARCHAR(100),
    temperature   FLOAT,
    windspeed     FLOAT,
    humidity      FLOAT,
    precipitation FLOAT,
    weathercode   INT,
    forecast_time TIMESTAMP
);