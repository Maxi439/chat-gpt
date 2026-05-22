import os
import sys
from dotenv import load_dotenv

load_dotenv()

from agents.tiktok_agent import run_tiktok_agent
from agents.funnel_agent import run_funnel_agent
from email_reporter import send_daily_report


def run_daily_agents() -> None:
    print("Starte TikTok-Agent...")
    tiktok_report = run_tiktok_agent()
    print("TikTok-Agent abgeschlossen.")

    print("Starte Funnel-Agent...")
    funnel_report = run_funnel_agent()
    print("Funnel-Agent abgeschlossen.")

    print("Sende E-Mail-Report...")
    send_daily_report(tiktok_report, funnel_report)
    print("Fertig!")


if __name__ == "__main__":
    run_daily_agents()
