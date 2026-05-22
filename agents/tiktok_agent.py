import anthropic
import os
from datetime import date


def run_tiktok_agent() -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = date.today().strftime("%d.%m.%Y")

    system_prompt = (
        "Du bist ein erfahrener TikTok-Content-Stratege und Copywriter. "
        "Deine Aufgabe ist es, täglich konkrete, umsetzbare TikTok-Content-Pläne zu erstellen. "
        "Du kennst aktuelle Trends, Hooks, und Storytelling-Techniken für TikTok. "
        "Deine Empfehlungen sind spezifisch, kreativ und auf virales Potential ausgerichtet."
    )

    user_prompt = (
        f"Heute ist der {today}. Erstelle einen vollständigen TikTok-Content-Plan für heute mit:\n\n"
        "1. **3 Video-Ideen** mit Titel, Hook (erste 3 Sekunden), Struktur und Call-to-Action\n"
        "2. **Trending Sounds/Musik** – welche Sounds gerade performen und passen könnten\n"
        "3. **Hashtag-Strategie** – 10-15 relevante Hashtags mit Erklärung\n"
        "4. **Optimaler Posting-Zeitplan** – wann und wie oft heute posten\n"
        "5. **Engagement-Taktiken** – wie auf Kommentare reagieren, Duets, Stitches nutzen\n"
        "6. **1 Skript** – vollständiges Wort-für-Wort-Skript für das viralste Video-Konzept\n\n"
        "Sei konkret und direkt umsetzbar. Keine generischen Tipps."
    )

    stream = client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=4000,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_prompt}],
    )

    with stream as s:
        result = s.get_final_message()

    output_parts = []
    for block in result.content:
        if block.type == "text":
            output_parts.append(block.text)

    return "\n".join(output_parts)
