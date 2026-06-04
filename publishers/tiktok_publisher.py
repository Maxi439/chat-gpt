"""TikTok publisher via TikTok Content Posting API v2."""
import time
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import config
from database.models import ContentItem
from .base_publisher import BasePublisher

_BASE = "https://open.tiktokapis.com/v2"


class TikTokPublisher(BasePublisher):
    platform = "tiktok"

    def __init__(self):
        self.open_id = config.TIKTOK_OPEN_ID
        self.token = config.TIKTOK_ACCESS_TOKEN

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=UTF-8",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
    def publish(self, item: ContentItem, video_path: str) -> str:
        """
        Uploads a video file and returns the TikTok publish_id.
        Uses the direct-post (file upload) flow.
        """
        self._validate_video(video_path)
        import os

        file_size = os.path.getsize(video_path)

        # Step 1: init upload
        init_resp = requests.post(
            f"{_BASE}/post/publish/video/init/",
            headers=self._headers,
            json={
                "post_info": {
                    "title": item.caption_tiktok[:150],
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                    "disable_duet": False,
                    "disable_comment": False,
                    "disable_stitch": False,
                    "video_cover_timestamp_ms": 1000,
                },
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": file_size,
                    "chunk_size": file_size,
                    "total_chunk_count": 1,
                },
            },
            timeout=30,
        )
        init_resp.raise_for_status()
        data = init_resp.json()["data"]
        publish_id = data["publish_id"]
        upload_url = data["upload_url"]

        # Step 2: upload file
        with open(video_path, "rb") as f:
            upload_resp = requests.put(
                upload_url,
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
                },
                data=f,
                timeout=120,
            )
        upload_resp.raise_for_status()

        # Step 3: poll status
        self._wait_for_ready(publish_id)
        return publish_id

    def _wait_for_ready(self, publish_id: str, timeout: int = 120) -> None:
        deadline = time.time() + timeout
        while time.time() < deadline:
            resp = requests.post(
                f"{_BASE}/post/publish/status/fetch/",
                headers=self._headers,
                json={"publish_id": publish_id},
                timeout=15,
            )
            resp.raise_for_status()
            status = resp.json()["data"]["status"]
            if status == "PUBLISH_COMPLETE":
                return
            if status in ("FAILED", "SPAM_RISK_TOO_HIGH_VIDEO_REJECTED"):
                raise RuntimeError(f"TikTok publish {publish_id} failed: {status}")
            time.sleep(5)
        raise TimeoutError(f"TikTok publish {publish_id} not ready after {timeout}s")

    def fetch_metrics(self, video_id: str) -> dict:
        resp = requests.post(
            f"{_BASE}/video/query/",
            headers=self._headers,
            json={
                "filters": {"video_ids": [video_id]},
                "fields": ["view_count", "like_count", "comment_count", "share_count"],
            },
            timeout=15,
        )
        resp.raise_for_status()
        v = resp.json()["data"]["videos"][0] if resp.json()["data"]["videos"] else {}
        total = v.get("view_count", 1) or 1
        v["engagement_rate"] = round(
            (v.get("like_count", 0) + v.get("comment_count", 0) + v.get("share_count", 0))
            / total * 100,
            2,
        )
        return v
