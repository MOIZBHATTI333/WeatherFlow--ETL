# transform.py
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta

def transform(date=None):
    if not date:
        date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    all_rows = []
    
    for filepath in Path("data/raw").glob(f"*_{date}.json"):
        with open(filepath) as f:
            raw = json.load(f)
        
        city = raw["city"]
        hourly = raw["hourly"]
        
        # turn the API's column-based format into rows
        df = pd.DataFrame({
            "city":         city,
            "observed_at":  hourly["time"],
            "temp_c":       hourly["temperature_2m"],
            "precipitation":hourly["precipitation"],
            "wind_kph":     hourly["windspeed_10m"],
            "humidity_pct": hourly["relativehumidity_2m"],
            "weathercode":  hourly.get("weathercode", [None]*len(hourly["time"])),  # add weathercode
        })
        
        # --- clean: handle nulls ---
        df["temp_c"]        = pd.to_numeric(df["temp_c"], errors="coerce")
        df["precipitation"] = pd.to_numeric(df["precipitation"], errors="coerce").fillna(0)
        df["wind_kph"]      = pd.to_numeric(df["wind_kph"], errors="coerce")
        df["humidity_pct"]  = pd.to_numeric(df["humidity_pct"], errors="coerce")
        df["weathercode"]   = pd.to_numeric(df["weathercode"], errors="coerce")  # clean weathercode
        
        # --- clean: fix types ---
        df["observed_at"] = pd.to_datetime(df["observed_at"])
        df["date"]        = df["observed_at"].dt.date
        df["hour"]        = df["observed_at"].dt.hour
        
        # --- enrich: derived columns ---
        df["temp_f"]    = (df["temp_c"] * 9/5) + 32
        df["is_raining"] = df["precipitation"] > 0
        
        # flag suspicious data instead of dropping it
        df["is_suspect"] = df["temp_c"].abs() > 60
        
        df["loaded_at"] = datetime.utcnow()
        
        all_rows.append(df)
        print(f"Transformed {city}: {len(df)} rows")
    
    final = pd.concat(all_rows, ignore_index=True)
    print(f"\nTotal rows: {len(final)}")
    return final

if __name__ == "__main__":
    df = transform()
    print(df.head())