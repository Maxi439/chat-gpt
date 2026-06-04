"""Fetches and stores performance metrics for published content."""
from datetime import datetime
import logging
from database.db import get_session
from database.models import PublishRecord, PerformanceMetric
from publishers.instagram_publisher import InstagramPublisher
from publishers.tiktok_publisher import TikTokPublisher
from publishers.youtube_publisher import YouTubePublisher

logger = logging.getLogger(__name__)

_FETCHERS = {
    "instagram": lambda pub_id: InstagramPublisher().fetch_metrics(pub_id),
    "tiktok": lambda pub_id: TikTokPublisher().fetch_metrics(pub_id),
    "youtube": lambda pub_id: YouTubePublisher().fetch_metrics(pub_id),
}


def collect_metrics() -> list[dict]:
    """
    Fetches latest metrics for all successful publish records
    and stores them in the DB. Returns a summary list.
    """
    summary = []
    with get_session() as session:
        records = (
            session.query(PublishRecord)
            .filter(
                PublishRecord.success == True,
                PublishRecord.platform_post_id.isnot(None),
            )
            .all()
        )

        for rec in records:
            fetcher = _FETCHERS.get(rec.platform)
            if not fetcher:
                continue
            try:
                data = fetcher(rec.platform_post_id)
                metric = PerformanceMetric(
                    publish_record_id=rec.id,
                    platform=rec.platform,
                    measured_at=datetime.utcnow(),
                    views=int(data.get("view_count") or data.get("plays") or data.get("viewCount", 0)),
                    likes=int(data.get("like_count") or data.get("likes") or data.get("likeCount", 0)),
                    comments=int(data.get("comment_count") or data.get("comments") or data.get("commentCount", 0)),
                    shares=int(data.get("share_count") or data.get("shares", 0)),
                    saves=int(data.get("saved", 0)),
                    reach=int(data.get("reach", 0)),
                    engagement_rate=float(data.get("engagement_rate", 0.0)),
                    raw_data=data,
                )
                session.add(metric)
                summary.append({
                    "platform": rec.platform,
                    "post_id": rec.platform_post_id,
                    "engagement_rate": metric.engagement_rate,
                    "views": metric.views,
                })
                logger.info(
                    f"[tracker] {rec.platform} {rec.platform_post_id}: "
                    f"{metric.views} views, {metric.engagement_rate}% engagement"
                )
            except Exception as exc:
                logger.warning(f"[tracker] Failed for {rec.platform}/{rec.platform_post_id}: {exc}")

    return summary


def top_performers(limit: int = 5) -> list[dict]:
    """Returns the top-performing posts by engagement rate."""
    with get_session() as session:
        rows = (
            session.query(PerformanceMetric)
            .order_by(PerformanceMetric.engagement_rate.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "platform": r.platform,
                "publish_record_id": r.publish_record_id,
                "engagement_rate": r.engagement_rate,
                "views": r.views,
                "likes": r.likes,
                "measured_at": r.measured_at.isoformat(),
            }
            for r in rows
        ]
