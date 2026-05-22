import os
import time
import schedule
from dotenv import load_dotenv

load_dotenv()

from main import run_daily_agents


def start_scheduler() -> None:
    run_time = os.environ.get("DAILY_RUN_TIME", "08:00")
    schedule.every().day.at(run_time).do(run_daily_agents)
    print(f"Scheduler gestartet – läuft täglich um {run_time} Uhr.")
    print("Drücke Ctrl+C zum Beenden.\n")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    start_scheduler()
