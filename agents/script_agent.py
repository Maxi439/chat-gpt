"""Generates platform-optimised video scripts from research data."""
import anthropic
import config

_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

_SYSTEM = """Du bist ein erfahrener Social-Media-Texter für Finanz- und Steuerbildungs-Content.
Du schreibst Skripte, die komplex klingende Steuergesetze einfach, verständlich
und unterhaltsam erklären. Deine Texte sind:
- Direkt adressierend (Du/Sie-Form einheitlich)
- Mit starkem Hook in den ersten 3 Sekunden
- Mit klarem Call-to-Action am Ende
- Vollständig auf Deutsch"""

_SCRIPT_TOOL = {
    "name": "generate_scripts",
    "description": "Generiert Video-Skripte für verschiedene Plattformen",
    "input_schema": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Klickstarker Video-Titel (max 70 Zeichen)",
            },
            "script_short": {
                "type": "string",
                "description": (
                    "Skript für TikTok/Instagram Reel (45-60 Sekunden, ca. 120-160 Wörter). "
                    "Format: HOOK → KERN-AUSSAGE → CTA"
                ),
            },
            "script_long": {
                "type": "string",
                "description": (
                    "Skript für YouTube (5-8 Minuten, ca. 700-1000 Wörter). "
                    "Format: HOOK → PROBLEM → LÖSUNG/ERKLÄRUNG → BEISPIEL → CTA"
                ),
            },
            "caption_instagram": {
                "type": "string",
                "description": (
                    "Instagram Caption (max 2200 Zeichen): "
                    "2-3 Teaser-Sätze + Mehrwert-Punkte + CTA + Hashtag-Platzhalter {{HASHTAGS}}"
                ),
            },
            "caption_tiktok": {
                "type": "string",
                "description": (
                    "TikTok Caption (max 150 Zeichen inkl. Hashtags): "
                    "Knackiger Satz + Hashtag-Platzhalter {{HASHTAGS}}"
                ),
            },
            "description_youtube": {
                "type": "string",
                "description": (
                    "YouTube Beschreibung (max 5000 Zeichen): "
                    "Erklärung + Timestamps + Links + Disclaimer"
                ),
            },
        },
        "required": [
            "title", "script_short", "script_long",
            "caption_instagram", "caption_tiktok", "description_youtube",
        ],
    },
}


def generate_scripts(research: dict) -> dict:
    """Takes research dict, returns scripts for all three platforms."""
    prompt = f"""Erstelle Video-Skripte und Captions basierend auf folgender Recherche:

**Thema:** {research["topic"]}
**Hook-Winkel:** {research["hook_angle"]}
**Kernfakten:**
{chr(10).join(f'- {f}' for f in research["key_facts"])}
**Anleger-Vorteile:**
{chr(10).join(f'- {b}' for b in research["investor_benefits"])}
**5-Jahres-Ausblick:** {research["five_year_outlook"]}
**Häufige Fehler:**
{chr(10).join(f'- {m}' for m in research["common_mistakes"])}
**Rechtliche Referenzen:** {", ".join(research["legal_references"])}

Verwende das Tool generate_scripts für die strukturierte Ausgabe.
Wichtig: Caption-Platzhalter {{{{HASHTAGS}}}} an passender Stelle einfügen."""

    response = _client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=4096,
        system=_SYSTEM,
        tools=[_SCRIPT_TOOL],
        tool_choice={"type": "tool", "name": "generate_scripts"},
        messages=[{"role": "user", "content": prompt}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "generate_scripts":
            return block.input

    raise ValueError("script_agent: no tool result returned")
