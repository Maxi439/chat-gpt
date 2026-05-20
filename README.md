# Immo Privat – Real Estate Lead Funnel

Zero-budget digital lead funnel for European real estate brokers. Captures, qualifies, and routes high-value leads from a landing page through an automated webhook pipeline to instant mobile alerts.

---

## Architecture

```
Tally.so Form  →  Make.com Webhook  →  Router
    ↑                                     ├── Urgency ≥ 4 + Equity verified → Telegram Alert
Landing Page                              └── All other leads → Google Sheets
    ↑
Social Media / WhatsApp Broadcasts
```

---

## File Structure

```
├── landing/
│   └── index.html                        # Landing page (German, mobile-first)
├── automation/
│   ├── make-blueprint.json               # Make.com scenario export (import directly)
│   └── telegram-alert-template.md        # Bot setup + alert configuration
└── marketing/
    ├── whatsapp-broadcast-setup.md        # WhatsApp Business + 5 message templates
    └── social-media-content-templates.md  # 10 Reels/TikTok scripts (DE + EN)
```

---

## Setup Instructions

### Step 1 – Landing Page

1. Deploy `landing/index.html` to any static host (Framer, Carrd, Netlify, GitHub Pages — free tier works)
2. Replace the two `https://tally.so` href values with your actual Tally form URL
3. Replace `Immo Privat` with your brand name throughout

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
