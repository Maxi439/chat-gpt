# Real Estate Lead Generation Funnel — European Market

## Overview

Zero-budget digital lead funnel for European real estate brokers. Captures, qualifies, and routes high-value leads from a landing page through an automated webhook pipeline to instant mobile alerts.

**Value proposition:** KI-Immobilienbewertung & Off-Market-Zugang in 120 Sekunden  
**Target audience:** High-net-worth property sellers and qualified buyers (Germany / DACH region)  
**Compliance:** GDPR-compliant throughout — explicit opt-in, no data sharing without consent  
**Automation platform:** Make.com (EU zone)  
**Primary language:** German (user-facing), English (technical documentation)

---

## Architecture

```
Landing Page (landing/index.html)
        │
        ▼ CTA click
Tally.so Qualification Form  ◄─── Social Media / WhatsApp Broadcasts drive traffic
        │
        ▼ webhook POST
Make.com Scenario (automation/make-blueprint.json)
        │
        ├── urgency_level ≥ 4 AND equity_status == "verified"
        │        └── Telegram Bot alert → respond within 15 minutes
        │
        └── all other leads
                 └── Google Sheets (nurture queue → manual follow-up)
```

| Layer | Technology | File |
|---|---|---|
| Landing page | Pure HTML/CSS, no JS frameworks, mobile-first | `landing/index.html` |
| Lead capture | Tally.so (external) | — |
| Automation engine | Make.com scenario | `automation/make-blueprint.json` |
| High-priority alert | Telegram Bot API via HTTP POST | `automation/telegram-alert-template.md` |
| Lead database | Google Sheets (via Make.com) | configured in scenario |
| Broadcast outreach | WhatsApp Business app | `marketing/whatsapp-broadcast-setup.md` |
| Content marketing | Instagram Reels / TikTok scripts | `marketing/social-media-content-templates.md` |

---

## File Structure

```
/
├── landing/
│   └── index.html                         # Landing page (German, dark/premium, mobile-first, no external JS)
│
├── automation/
│   ├── make-blueprint.json                # Make.com scenario — Tally webhook → Router → Telegram / Sheets
│   └── telegram-alert-template.md         # Bot setup via @BotFather, HTTP module config, German alert template
│
├── marketing/
│   ├── whatsapp-broadcast-setup.md        # WhatsApp Business setup, 3 broadcast segments, 5 templates, GDPR
│   └── social-media-content-templates.md  # 10 Reels/TikTok scripts (DE + EN), production notes
│
└── README.md                              # This file — overview, architecture, setup, file map
```

---

## Setup Instructions — Tally → Make.com → Telegram

### Step 1 – Landing Page

1. Deploy `landing/index.html` to any static host (Framer, Carrd, Netlify, GitHub Pages — free tier works)
2. Replace the two `https://tally.so` href values with your actual Tally form URL
3. Replace `Immo Privat` with your brand name throughout
4. Update the footer Impressum and Datenschutz links to your actual legal pages

### Step 2 – Tally.so Qualification Form

Create a free form at [tally.so](https://tally.so) with these fields:

| Field Name (use exact) | Type | Notes |
|---|---|---|
| `name` | Short text | |
| `email` | Email | |
| `phone` | Phone | |
| `urgency_level` | Number (1–5) | 5 = immediate |
| `equity_status` | Dropdown | Options: `verified`, `unverified` |
| `property_type` | Dropdown | Multi-family, Commercial, Residential, Land |
| `location` | Short text | City / region |
| `estimated_value` | Short text | |

Enable **Webhooks** in Tally → Integrations → copy the Make.com webhook URL into the endpoint field.

### Step 3 – Make.com Automation

1. Create a free account at [make.com](https://make.com) (EU zone: eu1.make.com)
2. New scenario → Import blueprint → upload `automation/make-blueprint.json`
3. Replace all `YOUR_` placeholders:

| Placeholder | Where to find it |
|---|---|
| `YOUR_MAKE_WEBHOOK_ID` | Auto-assigned after import — copy from the Webhook trigger module |
| `YOUR_TELEGRAM_BOT_TOKEN` | @BotFather on Telegram |
| `YOUR_TELEGRAM_CHAT_ID` | @userinfobot on Telegram |
| `YOUR_GOOGLE_SHEETS_SPREADSHEET_ID` | From the Google Sheets URL |
| `YOUR_GOOGLE_SHEETS_CONNECTION_ID` | Created when you connect Google account in Make.com |
| `YOUR_GOOGLE_SHEETS_SHEET_NAME` | Exact tab name in your spreadsheet |

See `automation/telegram-alert-template.md` for detailed Telegram configuration.

### Step 4 – WhatsApp Business

Follow `marketing/whatsapp-broadcast-setup.md` to set up broadcast lists and configure GDPR-compliant opt-in.

### Step 5 – Social Media

Use the 10 scripts in `marketing/social-media-content-templates.md` for daily Reels/TikTok content. Replace `Link in Bio` with your Tally form URL. Post 1× per day, Mon–Fri.

---

## Placeholder Reference

Every value that must be replaced before going live is prefixed with `YOUR_`:

| Placeholder | File(s) | What to enter |
|---|---|---|
| `https://tally.so` | `landing/index.html` | Your actual Tally form URL |
| `YOUR_MAKE_WEBHOOK_ID` | `make-blueprint.json` | Auto-assigned by Make after webhook creation |
| `YOUR_TELEGRAM_BOT_TOKEN` | `make-blueprint.json` | Token from @BotFather |
| `YOUR_TELEGRAM_CHAT_ID` | `make-blueprint.json` | Numeric chat ID (personal or group) |
| `YOUR_GOOGLE_SHEETS_SPREADSHEET_ID` | `make-blueprint.json` | ID from the Google Sheets URL |
| `YOUR_GOOGLE_SHEETS_CONNECTION_ID` | `make-blueprint.json` | Auto-assigned after Google OAuth in Make.com |
| `YOUR_GOOGLE_SHEETS_SHEET_NAME` | `make-blueprint.json` | Exact tab name in your spreadsheet |
| `[YOUR_TALLY_FORM_URL]` | `whatsapp-broadcast-setup.md`, `social-media-content-templates.md` | Your Tally form URL |

---

## GDPR Compliance Checklist

- [ ] Datenschutzerklärung (Privacy Policy) linked from landing page footer
- [ ] Impressum linked from landing page footer
- [ ] WhatsApp opt-in documented per contact before adding to broadcast lists
- [ ] Tally form includes consent checkbox referencing your privacy policy
- [ ] Make.com data processing on EU zone (eu1.make.com) — confirm in account settings
- [ ] Google Sheets access restricted to authorized accounts only

---

## Cost

| Tool | Tier | Monthly Cost |
|---|---|---|
| Landing page host | Netlify / GitHub Pages free | €0 |
| Tally.so | Free | €0 |
| Make.com | Free (1,000 ops/month) | €0 |
| WhatsApp Business | Free | €0 |
| **Total** | | **€0** |
