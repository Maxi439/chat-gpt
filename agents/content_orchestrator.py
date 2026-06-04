"""Orchestrates all agents to produce a complete ContentItem."""
from datetime import datetime
from database.db import get_session
from database.models import ContentItem
from . import research_agent, script_agent, thumbnail_agent, hashtag_agent
import config


def _inject_hashtags(caption: str, hashtags: list[str]) -> str:
    tag_str = " ".join(hashtags)
    return caption.replace("{{HASHTAGS}}", tag_str)


def produce_content(topic: str, jurisdiction: str = "DE") -> int:
    """
    Runs the full agent pipeline for one topic.
    Returns the ContentItem.id of the created draft.
    """
    print(f"[orchestrator] Researching: {topic}")
    research = research_agent.research_topic(topic, jurisdiction)

    print(f"[orchestrator] Writing scripts...")
    scripts = script_agent.generate_scripts(research)

    print(f"[orchestrator] Generating thumbnail specs...")
    thumb = thumbnail_agent.generate_thumbnail_specs(
        topic=topic,
        title=scripts["title"],
        hook_angle=research["hook_angle"],
    )

    print(f"[orchestrator] Generating hashtags...")
    tags = hashtag_agent.generate_hashtags(topic, scripts["title"])

    caption_ig = _inject_hashtags(
        scripts["caption_instagram"], tags["instagram"]
    )
    caption_tt = _inject_hashtags(
        scripts["caption_tiktok"], tags["tiktok"]
    )

    with get_session() as session:
        item = ContentItem(
            topic=topic,
            jurisdiction=jurisdiction,
            title=scripts["title"],
            script_short=scripts["script_short"],
            script_long=scripts["script_long"],
            thumbnail_prompt=thumb["dall_e_prompt"],
            hashtags_instagram=tags["instagram"],
            hashtags_tiktok=tags["tiktok"],
            tags_youtube=tags["youtube_tags"],
            caption_instagram=caption_ig,
            caption_tiktok=caption_tt,
            description_youtube=scripts["description_youtube"],
            status="draft",
        )
        session.add(item)
        session.flush()
        item_id = item.id

    print(f"[orchestrator] ContentItem #{item_id} saved as draft.")
    return item_id
