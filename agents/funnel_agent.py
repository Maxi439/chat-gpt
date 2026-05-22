import anthropic
import os
from datetime import date


def run_funnel_agent() -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = date.today().strftime("%d.%m.%Y")

    system_prompt = (
        "Du bist ein erfahrener Funnel-Optimierer und Online-Marketing-Experte. "
        "Du spezialisierst dich auf Conversion-Rate-Optimierung, Sales Funnels, "
        "Landing Pages, E-Mail-Sequenzen und Umsatzmaximierung. "
        "Du gibst konkrete, datengetriebene Empfehlungen zur Funnel-Verbesserung."
    )

    user_prompt = (
        f"Heute ist der {today}. Erstelle eine vollständige Funnel-Optimierungs-Analyse für heute:\n\n"
        "1. **Funnel-Audit-Checkliste** – die 10 wichtigsten Punkte, die jeden Tag überprüft werden sollten\n"
        "2. **Conversion-Optimierung** – 5 konkrete Maßnahmen zur sofortigen CRO-Verbesserung\n"
        "3. **Traffic-Qualität** – Strategien zur Verbesserung der Lead-Qualität\n"
        "4. **E-Mail-Sequenz-Optimierung** – Betreffzeilen, Timing, Segmentierung-Tipps\n"
        "5. **Upsell/Cross-Sell-Strategien** – konkrete Möglichkeiten den Warenkorb zu erhöhen\n"
        "6. **A/B-Test-Ideen** – 3 Tests, die diese Woche gestartet werden sollten\n"
        "7. **Tagesaufgabe** – die EINE wichtigste Aktion heute für maximalen Funnel-Impact\n\n"
        "Fokus auf sofortige Umsetzbarkeit und messbaren ROI. Keine Theorie, nur Praxis."
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
