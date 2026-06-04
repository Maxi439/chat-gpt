from abc import ABC, abstractmethod
from database.models import ContentItem


class BasePublisher(ABC):
    platform: str = ""

    @abstractmethod
    def publish(self, item: ContentItem, video_path: str) -> str:
        """Publishes the content and returns the platform post ID."""

    def _validate_video(self, video_path: str) -> None:
        import os
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
