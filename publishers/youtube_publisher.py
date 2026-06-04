"""YouTube Shorts + long-form publisher via YouTube Data API v3."""
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from tenacity import retry, stop_after_attempt, wait_exponential
import config
from database.models import ContentItem
from .base_publisher import BasePublisher


def _get_youtube_service():
    creds = Credentials(
        token=None,
        refresh_token=config.YOUTUBE_REFRESH_TOKEN,
        client_id=config.YOUTUBE_CLIENT_ID,
        client_secret=config.YOUTUBE_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token",
    )
    if not creds.valid:
        creds.refresh(Request())
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


class YouTubePublisher(BasePublisher):
    platform = "youtube"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
    def publish(self, item: ContentItem, video_path: str) -> str:
        """Uploads video and returns the YouTube video ID."""
        self._validate_video(video_path)
        youtube = _get_youtube_service()

        # Determine if this is a Short (≤60s) or regular video
        is_short = "#shorts" in item.description_youtube.lower()
        title = item.title[:100]
        if is_short and "#shorts" not in title.lower():
            title = title[:95] + " #Shorts"

        body = {
            "snippet": {
                "title": title,
                "description": item.description_youtube,
                "tags": item.tags_youtube,
                "categoryId": "27",  # Education
                "defaultLanguage": config.CONTENT_LANGUAGE,
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        }

        media = MediaFileUpload(
            video_path,
            mimetype="video/mp4",
            resumable=True,
            chunksize=1024 * 1024 * 8,
        )

        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media,
        )

        response = None
        while response is None:
            _, response = request.next_chunk()

        return response["id"]

    def fetch_metrics(self, video_id: str) -> dict:
        youtube = _get_youtube_service()
        resp = (
            youtube.videos()
            .list(part="statistics", id=video_id)
            .execute()
        )
        stats = resp["items"][0]["statistics"] if resp.get("items") else {}
        views = int(stats.get("viewCount", 1)) or 1
        stats["engagement_rate"] = round(
            (int(stats.get("likeCount", 0)) + int(stats.get("commentCount", 0)))
            / views * 100,
            2,
        )
        return stats
