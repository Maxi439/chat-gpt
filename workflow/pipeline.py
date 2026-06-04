"""End-to-end pipeline: content generation → publish → record."""
from datetime import datetime
from database.db import get_session
from database.models import ContentItem, PublishRecord
from agents.content_orchestrator import produce_content
from publishers.instagram_publisher import InstagramPublisher
from publishers.tiktok_publisher import TikTokPublisher
from publishers.youtube_publisher import YouTubePublisher
import config


_PUBLISHERS = {
    "instagram": InstagramPublisher,
    "tiktok": TikTokPublisher,
    "youtube": YouTubePublisher,
}


def run_content_pipeline(
    topic: str,
    video_short_path: str = "",
    video_long_path: str = "",
    dry_run: bool = False,
) -> dict:
    """
    Full pipeline for one content piece.

    Parameters
    ----------
    topic          : Tax topic to cover.
    video_short_path: Path to 9:16 short video (TikTok / Instagram Reel).
    video_long_path : Path to 16:9 long video (YouTube).
    dry_run        : If True, generate content but skip publishing.

    Returns
    -------
    dict with content_item_id and per-platform publish results.
    """
    item_id = produce_content(topic, config.TAX_JURISDICTION)
    results: dict = {"content_item_id": item_id, "platforms": {}}

    if dry_run:
        print("[pipeline] dry_run=True – skipping publish step.")
        return results

    with get_session() as session:
        item = session.get(ContentItem, item_id)
        if item is None:
            raise ValueError(f"ContentItem #{item_id} not found")

        for platform, Publisher in _PUBLISHERS.items():
            video_path = (
                video_long_path if platform == "youtube" else video_short_path
            )

            record = PublishRecord(
                content_item_id=item_id,
                platform=platform,
            )

            try:
                pub = Publisher()
                post_id = pub.publish(item, video_path)
                record.platform_post_id = post_id
                record.published_at = datetime.utcnow()
                record.success = True
                print(f"[pipeline] Published on {platform}: {post_id}")
            except Exception as exc:
                record.success = False
                record.error_message = str(exc)
                print(f"[pipeline] ERROR on {platform}: {exc}")

            session.add(record)
            results["platforms"][platform] = {
                "success": record.success,
                "post_id": record.platform_post_id,
                "error": record.error_message,
            }

        item.status = (
            "published"
            if any(v["success"] for v in results["platforms"].values())
            else "failed"
        )

    return results
