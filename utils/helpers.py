"""Utility helpers shared across the project."""
import json
from pathlib import Path
from datetime import datetime


def save_draft_json(content_item_id: int, data: dict, output_dir: str = "drafts") -> str:
    """Saves a content draft to a JSON file for review before publishing."""
    Path(output_dir).mkdir(exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = f"{output_dir}/draft_{content_item_id}_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def truncate(text: str, max_len: int) -> str:
    """Truncates text to max_len, appending '…' if needed."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


def format_hashtags(tags: list[str], prefix: bool = True) -> str:
    if prefix:
        return " ".join(t if t.startswith("#") else f"#{t}" for t in tags)
    return " ".join(t.lstrip("#") for t in tags)
