import schedule
import time
from run_pipeline import run

def job():
    """Run the ETL pipeline to refresh weather data."""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting scheduled data refresh...")
    try:
        run()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Data refresh completed successfully.")
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error during data refresh: {e}")

def main():
    """Schedule the job to run every 30 minutes."""
    print("Weather Data Scheduler started. Refreshing data every 30 minutes...")
    print("Press Ctrl+C to stop.")

    # Schedule the job to run every 30 minutes
    schedule.every(30).minutes.do(job)

    # Run the job immediately on startup
    job()

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()