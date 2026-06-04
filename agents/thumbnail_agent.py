"""Generates thumbnail descriptions and text overlays for each platform."""
import anthropic
import config

_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

_SYSTEM = """Du bist ein Experte für Social-Media-Thumbnails und visuelle Kommunikation.
Du erstellst präzise Beschreibungen für Thumbnails, die maximale Click-Through-Rates erzielen.
Thumbnails müssen auf den ersten Blick das Interesse wecken und die Kernbotschaft vermitteln."""

_THUMBNAIL_TOOL = {
    "name": "generate_thumbnail_specs",
    "description": "Generiert detaillierte Thumbnail-Spezifikationen",
    "input_schema": {
        "type": "object",
        "properties": {
            "headline_text": {
                "type": "string",
                "description": "Haupttext auf dem Thumbnail (max 5 Wörter, sehr groß)",
            },
            "subtext": {
                "type": "string",
                "description": "Ergänzender Text (max 8 Wörter)",
            },
            "background_description": {
                "type": "string",
                "description": (
                    "Hintergrund-Beschreibung für KI-Bildgenerierung "
                    "(Farben, Stil, Symbole z.B. Geldscheine, Diagramme)"
                ),
            },
            "color_scheme": {
                "type": "string",
                "description": "Farbschema (z.B. 'Dunkelblau-Gold professionell' oder 'Grün-Weiß energetisch')",
            },
            "emoji_accents": {
                "type": "array",
                "items": {"type": "string"},
                "description": "2-3 passende Emojis als visuelle Akzente",
            },
            "dall_e_prompt": {
                "type": "string",
                "description": (
                    "Vollständiger DALL-E / Stable-Diffusion Prompt "
                    "für automatisierte Thumbnail-Generierung (Englisch)"
                ),
            },
            "a_b_variant": {
                "type": "string",
                "description": "Alternative Thumbnail-Idee für A/B-Test",
            },
        },
        "required": [
            "headline_text", "subtext", "background_description",
            "color_scheme", "emoji_accents", "dall_e_prompt", "a_b_variant",
        ],
    },
}


def generate_thumbnail_specs(topic: str, title: str, hook_angle: str) -> dict:
    """Returns thumbnail specifications for a given content piece."""
    prompt = (
        f"Erstelle Thumbnail-Spezifikationen für ein Video:\n"
        f"**Thema:** {topic}\n"
        f"**Titel:** {title}\n"
        f"**Hook-Winkel:** {hook_angle}\n\n"
        "Das Thumbnail soll professionell, klar und klickstark sein. "
        "Verwende das Tool generate_thumbnail_specs."
    )

    response = _client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=1024,
        system=_SYSTEM,
        tools=[_THUMBNAIL_TOOL],
        tool_choice={"type": "tool", "name": "generate_thumbnail_specs"},
        messages=[{"role": "user", "content": prompt}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "generate_thumbnail_specs":
            return block.input

    raise ValueError("thumbnail_agent: no tool result returned")
