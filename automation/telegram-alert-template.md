# Telegram Alert Setup – Immo Privat Lead Funnel

## 1. Create the Bot via @BotFather

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts
3. Choose a name (e.g. `Immo Privat Leads`) and a username ending in `bot` (e.g. `immoprivat_leads_bot`)
4. Copy the **API token** — format: `1234567890:AAF...` → this is `YOUR_TELEGRAM_BOT_TOKEN`

## 2. Find Your Chat ID

1. Search for **@userinfobot** in Telegram and send any message
2. It replies with your numeric user ID → this is `YOUR_TELEGRAM_CHAT_ID`

For a group chat: add the bot to the group, then send a message mentioning it.
Use `https://api.telegram.org/botYOUR_TOKEN/getUpdates` to see the group's chat_id (negative number).

## 3. Make.com HTTP Module Configuration

In your Make.com scenario, after the Router filter for high-priority leads:

| Field | Value |
|---|---|
| Module | **HTTP – Make a request** |
| URL | `https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/sendMessage` |
| Method | POST |
| Body type | Raw |
| Content type | JSON (application/json) |
| Parse response | Yes |

**Request body** (paste as-is, replace placeholders):

```json
{
  "chat_id": "YOUR_TELEGRAM_CHAT_ID",
  "parse_mode": "Markdown",
  "text": "*🔴 DRINGEND – Neuer Lead*\n\n*Name:* {{1.data.name}}\n*E-Mail:* {{1.data.email}}\n*Telefon:* {{1.data.phone}}\n*Dringlichkeit:* {{1.data.urgency_level}}/5\n*Eigenkapital:* {{1.data.equity_status}}\n*Objektart:* {{1.data.property_type}}\n*Standort:* {{1.data.location}}\n*Geschätzter Wert:* {{1.data.estimated_value}}\n\n_Eingegangen: {{now}}_"
}
```

> The `{{1.data.*}}` placeholders reference fields from your Tally webhook payload (Module 1 in Make.com). Verify exact field names in Make.com's run history after a test submission.

## 4. Alert Message Template

When a lead with urgency ≥ 4 and verified equity submits the form, you receive:

```
🔴 DRINGEND – Neuer Lead

Name: Max Mustermann
E-Mail: max@example.com
Telefon: +49 170 1234567
Dringlichkeit: 5/5
Eigenkapital: verified
Objektart: Mehrfamilienhaus
Standort: München
Geschätzter Wert: 2.500.000 €

Eingegangen: 20.05.2025 14:32
```

## 5. Notification Sound Configuration

### iOS Telegram
Settings → Notifications → Tap the bot chat → Sound → select a distinct tone (e.g. **Alert**)
Enable **Override Do Not Disturb** for this contact.

### Android Telegram
Long-press the bot chat → Notifications → Custom notification → Sound → choose a ringtone
Enable **Priority** to bypass silent mode.

### Recommended
Assign the bot to a dedicated notification sound different from all other apps so you recognise it immediately without looking at the screen.
