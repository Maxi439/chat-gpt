"""APScheduler-based scheduler – posts 3× per week."""
import itertools
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import config
from database.db import init_db
from .pipeline import run_content_pipeline

logger = logging.getLogger(__name__)

# Weekday abbreviations for cron (0=Mon, 6=Sun → APScheduler uses mon,tue,…)
_WEEKDAY_MAP = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}


def _make_cron_days(days: list[int]) -> str:
    return ",".join(_WEEKDAY_MAP[d] for d in days)


def _topic_cycle():
    """Infinite round-robin over the topic pool."""
    return itertools.cycle(config.TAX_TOPICS)


_topic_iter = _topic_cycle()


def _scheduled_job(video_short_path: str = "", video_long_path: str = "") -> None:
    topic = next(_topic_iter)
    logger.info(f"[scheduler] Triggered – topic: {topic}")
    try:
        result = run_content_pipeline(
            topic=topic,
            video_short_path=video_short_path,
            video_long_path=video_long_path,
            dry_run=(not video_short_path),
        )
        logger.info(f"[scheduler] Done: {result}")
    except Exception:
        logger.exception("[scheduler] Pipeline error")


def start_scheduler(
    video_short_path: str = "",
    video_long_path: str = "",
) -> None:
    """Starts the blocking scheduler. Call this from main.py."""
    init_db()

    hour, minute = config.POSTING_TIME_UTC.split(":")
    cron_days = _make_cron_days(config.POSTING_DAYS)

    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(
        func=_scheduled_job,
        trigger=CronTrigger(
            day_of_week=cron_days,
            hour=int(hour),
            minute=int(minute),
        ),
        kwargs={
            "video_short_path": video_short_path,
            "video_long_path": video_long_path,
        },
        id="tax_content_post",
        name="Tax Content Auto-Post",
        misfire_grace_time=3600,
        coalesce=True,
    )

    logger.info(
        f"[scheduler] Running – posting on {cron_days} at {hour}:{minute} UTC"
    )
    scheduler.start()
