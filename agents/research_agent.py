"""Researches current tax laws and investment-related regulations."""
import json
import anthropic
import config


_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

_SYSTEM = """Du bist ein spezialisierter Steuerrechts-Researcher für Deutschland.
Deine Aufgabe ist es, aktuelle, faktenbasierte Informationen zu steuerlichen Themen
zu liefern, die für Anleger und Investoren relevant sind.

Achte auf:
- Aktuelle Gesetzeslage (aktuelles Steuerjahr und nächste 5 Jahre Ausblick)
- Paragraphen-Referenzen (EStG, KStG, UStG, GewStG usw.)
- Praktische Relevanz für Privatanleger und Unternehmen
- Mögliche gesetzliche Änderungen / politische Diskussionen

Antworte ausschließlich in validem JSON."""

_RESEARCH_TOOL = {
    "name": "compile_tax_research",
    "description": "Kompiliert steuerliche Rechercheergebnisse zu einem Thema",
    "input_schema": {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "Das recherchierte Steuer-Thema"},
            "key_facts": {
                "type": "array",
                "items": {"type": "string"},
                "description": "5-8 wichtige Fakten/Regelungen zu diesem Thema",
            },
            "legal_references": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Relevante Paragraphen (z.B. '§7g EStG – Investitionsabzugsbetrag')",
            },
            "investor_benefits": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Konkrete Vorteile/Ersparnisse für Anleger",
            },
            "five_year_outlook": {
                "type": "string",
                "description": "Ausblick: Was ändert sich in den nächsten 5 Jahren?",
            },
            "common_mistakes": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Häufige Fehler, die Anleger bei diesem Thema machen",
            },
            "hook_angle": {
                "type": "string",
                "description": "Überraschender/provokanter Einstieg für Social-Media-Videos",
            },
        },
        "required": [
            "topic", "key_facts", "legal_references",
            "investor_benefits", "five_year_outlook",
            "common_mistakes", "hook_angle",
        ],
    },
}


def research_topic(topic: str, jurisdiction: str = "DE") -> dict:
    """Returns structured research data for a given tax topic."""
    prompt = (
        f"Recherchiere das folgende steuerliche Thema für {jurisdiction}: **{topic}**\n\n"
        "Verwende das Tool compile_tax_research, um deine Ergebnisse strukturiert zurückzugeben."
    )

    response = _client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=2048,
        system=_SYSTEM,
        tools=[_RESEARCH_TOOL],
        tool_choice={"type": "tool", "name": "compile_tax_research"},
        messages=[{"role": "user", "content": prompt}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "compile_tax_research":
            return block.input

    raise ValueError(f"research_agent: no tool result for topic '{topic}'")
