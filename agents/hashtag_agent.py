"""Generates platform-optimised hashtag sets from topic and content data."""
import anthropic
import config
from config import HASHTAGS as BASE_HASHTAGS

_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

_SYSTEM = """Du bist ein Social-Media-Algorithmus-Experte.
Du wählst und ergänzt Hashtag-Sets, die maximale Reichweite erzielen.
Strategisch: Mischung aus großen (>1M Posts), mittelgroßen (100k-1M) und Nischen-Hashtags."""

_HASHTAG_TOOL = {
    "name": "generate_hashtags",
    "description": "Generiert optimierte Hashtag-Sets für alle Plattformen",
    "input_schema": {
        "type": "object",
        "properties": {
            "instagram": {
                "type": "array",
                "items": {"type": "string"},
                "description": "25-30 Instagram Hashtags (mit #)",
            },
            "tiktok": {
                "type": "array",
                "items": {"type": "string"},
                "description": "8-10 TikTok Hashtags (mit #)",
            },
            "youtube_tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "10-15 YouTube Tags (ohne #, Schlüsselwörter)",
            },
            "best_posting_times": {
                "type": "object",
                "properties": {
                    "instagram": {"type": "string"},
                    "tiktok": {"type": "string"},
                    "youtube": {"type": "string"},
                },
                "description": "Empfohlene Posting-Zeiten für jede Plattform (Uhrzeit UTC+1)",
            },
        },
        "required": ["instagram", "tiktok", "youtube_tags", "best_posting_times"],
    },
}


def generate_hashtags(topic: str, title: str) -> dict:
    """Returns platform-specific hashtag sets for the given content."""
    base = {
        "instagram": BASE_HASHTAGS["instagram"],
        "tiktok": BASE_HASHTAGS["tiktok"],
        "youtube": BASE_HASHTAGS["youtube"],
    }

    prompt = (
        f"Erstelle optimierte Hashtag-Sets für folgendes Video:\n"
        f"**Thema:** {topic}\n"
        f"**Titel:** {title}\n\n"
        f"Basis-Hashtags zur Inspiration:\n"
        f"Instagram: {', '.join(base['instagram'][:8])}\n"
        f"TikTok: {', '.join(base['tiktok'][:5])}\n"
        f"YouTube: {', '.join(base['youtube'][:5])}\n\n"
        "Ergänze und optimiere diese Sets. "
        "Verwende das Tool generate_hashtags."
    )

    response = _client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=1024,
        system=_SYSTEM,
        tools=[_HASHTAG_TOOL],
        tool_choice={"type": "tool", "name": "generate_hashtags"},
        messages=[{"role": "user", "content": prompt}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "generate_hashtags":
            return block.input

    raise ValueError("hashtag_agent: no tool result returned")
