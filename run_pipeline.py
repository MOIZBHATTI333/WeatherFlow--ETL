# run_pipeline.py
from extract import extract
from transform import transform
from load import create_tables, load_weather_data

def run():
    print("=== STEP 0: Create Tables ===")
    create_tables()
    
    print("=== STEP 1: Extract ===")
    extract()
    
    print("\n=== STEP 2: Transform ===")
    df = transform()
    
    print("\n=== STEP 3: Load ===")
    load_weather_data(df)
    
    print("\nPipeline complete.")

if __name__ == "__main__":
    run()