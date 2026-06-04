import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
CLAUDE_MODEL = "claude-sonnet-4-6"

INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")

TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "")
TIKTOK_OPEN_ID = os.getenv("TIKTOK_OPEN_ID", "")

YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "")

POSTING_DAYS = [int(d) for d in os.getenv("POSTING_DAYS", "1,3,5").split(",")]
POSTING_TIME_UTC = os.getenv("POSTING_TIME_UTC", "09:00")
CONTENT_LANGUAGE = os.getenv("CONTENT_LANGUAGE", "de")
TAX_JURISDICTION = os.getenv("TAX_JURISDICTION", "DE")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tax_content.db")

# Tax topics pool – rotated across the weekly schedule
TAX_TOPICS = [
    "Abschreibungen auf Investitionsgüter (AfA)",
    "Investitionsabzugsbetrag (IAB) §7g EStG",
    "Gewerbesteuerhebesatz und Optimierung",
    "Holding-Struktur für Steueroptimierung",
    "Immobilien: Steuerliche Abschreibung & Verlustverrechnung",
    "ETF & Fonds: Vorabpauschale und Teilfreistellung",
    "Verlustverrechnungstöpfe clever nutzen",
    "Grunderwerbsteuer umgehen durch Share Deal",
    "Kryptowährungen: Steuerliche Behandlung 2024/2025",
    "Betriebliche Altersvorsorge: Steuervorteile",
    "Sonderabschreibungen für kleine Unternehmen",
    "Steuerliche Behandlung von Dividenden",
    "Verlustvorträge optimal einsetzen",
    "Förderungen und steuerfreie Zulagen (z.B. BAFA, KfW)",
    "GmbH vs. Einzelunternehmen: Steuervergleich",
]

# Hashtag pools per platform
HASHTAGS = {
    "instagram": [
        "#Steuertipps", "#Investieren", "#Finanzbildung", "#Steueroptimierung",
        "#Kapitalanlage", "#Finanztipps", "#Vermögensaufbau", "#Steuern",
        "#Wirtschaft", "#Geldanlage", "#ETF", "#Immobilieninvestition",
        "#Finanzielle Freiheit", "#Altersvorsorge", "#Steuerrecht",
    ],
    "tiktok": [
        "#Steuertipps", "#Finanzbildung", "#Investieren", "#Geldtipps",
        "#Steuern", "#ETF", "#Vermögensaufbau", "#Finanzen",
        "#GeldVerdienen", "#Kapitalanlage",
    ],
    "youtube": [
        "Steuertipps", "Steueroptimierung", "Investieren Deutschland",
        "Finanzbildung", "Kapitalanlage", "ETF Steuern",
        "Immobilien Steuern", "GmbH Steuervorteile", "Krypto Steuern",
        "Vermögensaufbau", "Finanzielle Freiheit",
    ],
}

PLATFORM_SPECS = {
    "instagram": {
        "max_caption_chars": 2200,
        "max_hashtags": 30,
        "video_duration_sec": (15, 90),
        "aspect_ratio": "9:16",
    },
    "tiktok": {
        "max_caption_chars": 2200,
        "max_hashtags": 10,
        "video_duration_sec": (15, 180),
        "aspect_ratio": "9:16",
    },
    "youtube": {
        "max_description_chars": 5000,
        "max_tags": 500,
        "video_duration_sec": (60, 600),
        "aspect_ratio": "16:9",
    },
}
