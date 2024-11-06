import schedule
import time
import sys
import os

# Add the root directory to the PYTHONPATH so it can find the backend module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the function to be scheduled
from backend.data_handler import extract_data_from_excel

# Define the schedule for calling the function every 8 seconds
schedule.every(8).seconds.do(extract_data_from_excel)

if __name__ == "__main__":
    print("Starting scheduler to extract data from Excel every 8 seconds...")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Sleep for a short duration to prevent excessive CPU usage
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
