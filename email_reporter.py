import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date


def send_daily_report(tiktok_report: str, funnel_report: str) -> None:
    sender = os.environ["EMAIL_SENDER"]
    password = os.environ["EMAIL_PASSWORD"]
    recipient = os.environ.get("EMAIL_RECIPIENT", "y.buchiha@gmail.com")
    today = date.today().strftime("%d.%m.%Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Dein täglicher Agenten-Report – {today}"
    msg["From"] = sender
    msg["To"] = recipient

    plain_text = _build_plain_text(today, tiktok_report, funnel_report)
    html_text = _build_html(today, tiktok_report, funnel_report)

    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_text, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"Report gesendet an {recipient}")


def _build_plain_text(today: str, tiktok: str, funnel: str) -> str:
    return (
        f"TÄGLICHER AGENTEN-REPORT – {today}\n"
        f"{'=' * 60}\n\n"
        f"TIKTOK-CONTENT-PLAN\n"
        f"{'-' * 40}\n"
        f"{tiktok}\n\n"
        f"{'=' * 60}\n\n"
        f"FUNNEL-OPTIMIERUNG\n"
        f"{'-' * 40}\n"
        f"{funnel}\n"
    )


def _build_html(today: str, tiktok: str, funnel: str) -> str:
    tiktok_html = _markdown_to_html(tiktok)
    funnel_html = _markdown_to_html(funnel)

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
  h1 {{ color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 10px; }}
  h2 {{ color: #16213e; background: #f0f0f0; padding: 10px 15px; border-radius: 5px; }}
  h3 {{ color: #0f3460; }}
  .section {{ margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
  .tiktok {{ border-left: 5px solid #ff0050; }}
  .funnel {{ border-left: 5px solid #00c2cb; }}
  .date {{ color: #666; font-size: 14px; }}
  strong {{ color: #e94560; }}
  ul, ol {{ line-height: 1.8; }}
</style>
</head>
<body>
  <h1>Täglicher Agenten-Report</h1>
  <p class="date">{today}</p>

  <div class="section tiktok">
    <h2>TikTok-Content-Plan</h2>
    {tiktok_html}
  </div>

  <div class="section funnel">
    <h2>Funnel-Optimierung</h2>
    {funnel_html}
  </div>
</body>
</html>"""


def _markdown_to_html(text: str) -> str:
    import re

    lines = text.split("\n")
    html_lines = []
    in_list = False
    in_ol = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            html_lines.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            html_lines.append(f"<h3>{stripped[3:]}</h3>")
        elif re.match(r"^\d+\. ", stripped):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            content = re.sub(r"^\d+\. ", "", stripped)
            content = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", content)
            html_lines.append(f"<li>{content}</li>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = stripped[2:]
            content = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", content)
            html_lines.append(f"<li>{content}</li>")
        elif stripped == "":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            html_lines.append("<br>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            line_html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", stripped)
            html_lines.append(f"<p>{line_html}</p>")

    if in_list:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")

    return "\n".join(html_lines)
