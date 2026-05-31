# extract.py
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path

CITIES = {
    "karachi":   {"lat": 24.86, "lon": 67.01},
    "Rawalpindi":  {"lat": 33.5973, "lon": 73.0479},
    "Lahore":  {"lat": 31.558, "lon": 74.3507},
    "Islamabad":   {"lat": 33.7215, "lon": 73.0433},
    "Faisalabad":   {"lat": 31.4155, "lon": 73.0897},
    "Mandi Bahauddin":   {"lat": 32.587, "lon": 73.4912},
}

def fetch_city_weather(city, lat, lon, date):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,windspeed_10m,relativehumidity_2m,weathercode",
        "start_date": date,
        "end_date": date,
        "timezone": "UTC"
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()   # raises an error if request fails
    data = response.json()
    data["city"] = city           # tag it before saving
    return data

def extract(date=None):
    if not date:
        # default: yesterday's complete data
        date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # save raw files — always keep the original data
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    
    results = []
    for city, coords in CITIES.items():
        print(f"Fetching {city}...")
        try:
            data = fetch_city_weather(city, coords["lat"], coords["lon"], date)
            # save raw JSON for auditing
            with open(f"data/raw/{city}_{date}.json", "w") as f:
                json.dump(data, f)
            results.append(data)
            print(f"  Done: {city}")
        except Exception as e:
            print(f"  Failed: {city} — {e}")
    
    return results

if __name__ == "__main__":
    extract()