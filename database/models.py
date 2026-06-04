from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, Enum, JSON
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(Integer, primary_key=True)
    topic = Column(String(256), nullable=False)
    jurisdiction = Column(String(8), default="DE")
    script_short = Column(Text)   # ≤60-sec script (TikTok/Instagram Reel)
    script_long = Column(Text)    # ≤10-min script (YouTube)
    thumbnail_prompt = Column(Text)
    hashtags_instagram = Column(JSON)
    hashtags_tiktok = Column(JSON)
    tags_youtube = Column(JSON)
    title = Column(String(256))
    description_youtube = Column(Text)
    caption_instagram = Column(Text)
    caption_tiktok = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(
        Enum("draft", "scheduled", "published", "failed", name="content_status"),
        default="draft",
    )
    scheduled_for = Column(DateTime, nullable=True)


class PublishRecord(Base):
    __tablename__ = "publish_records"

    id = Column(Integer, primary_key=True)
    content_item_id = Column(Integer, nullable=False)
    platform = Column(String(32), nullable=False)
    platform_post_id = Column(String(256), nullable=True)
    published_at = Column(DateTime, nullable=True)
    success = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)


class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    id = Column(Integer, primary_key=True)
    publish_record_id = Column(Integer, nullable=False)
    platform = Column(String(32), nullable=False)
    measured_at = Column(DateTime, default=datetime.utcnow)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    raw_data = Column(JSON, nullable=True)
