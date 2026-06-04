"""Instagram Reels publisher via Meta Graph API."""
import time
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import config
from database.models import ContentItem
from .base_publisher import BasePublisher

_BASE = "https://graph.facebook.com/v19.0"


class InstagramPublisher(BasePublisher):
    platform = "instagram"

    def __init__(self):
        self.account_id = config.INSTAGRAM_ACCOUNT_ID
        self.token = config.INSTAGRAM_ACCESS_TOKEN

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
    def publish(self, item: ContentItem, video_url: str) -> str:
        """
        video_url must be a publicly accessible URL for the Reel video.
        Returns the Instagram media ID.
        """
        # Step 1: create media container
        container_resp = requests.post(
            f"{_BASE}/{self.account_id}/reels",
            params={
                "video_url": video_url,
                "caption": item.caption_instagram,
                "share_to_feed": "true",
                "access_token": self.token,
            },
            timeout=30,
        )
        container_resp.raise_for_status()
        container_id = container_resp.json()["id"]

        # Step 2: poll until video is ready
        self._wait_for_ready(container_id)

        # Step 3: publish
        publish_resp = requests.post(
            f"{_BASE}/{self.account_id}/media_publish",
            params={
                "creation_id": container_id,
                "access_token": self.token,
            },
            timeout=30,
        )
        publish_resp.raise_for_status()
        return publish_resp.json()["id"]

    def _wait_for_ready(self, container_id: str, timeout: int = 120) -> None:
        deadline = time.time() + timeout
        while time.time() < deadline:
            resp = requests.get(
                f"{_BASE}/{container_id}",
                params={
                    "fields": "status_code",
                    "access_token": self.token,
                },
                timeout=15,
            )
            resp.raise_for_status()
            status = resp.json().get("status_code")
            if status == "FINISHED":
                return
            if status == "ERROR":
                raise RuntimeError(f"Instagram container {container_id} failed")
            time.sleep(5)
        raise TimeoutError(f"Instagram container {container_id} not ready after {timeout}s")

    def fetch_metrics(self, post_id: str) -> dict:
        resp = requests.get(
            f"{_BASE}/{post_id}/insights",
            params={
                "metric": "plays,likes,comments,shares,saved,reach",
                "access_token": self.token,
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = {m["name"]: m["values"][0]["value"] for m in resp.json().get("data", [])}
        total = data.get("plays", 1) or 1
        data["engagement_rate"] = round(
            (data.get("likes", 0) + data.get("comments", 0) + data.get("shares", 0))
            / total * 100,
            2,
        )
        return data
