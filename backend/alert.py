"""
alert.py

Purpose:
- Send email alerts when high-risk activity is detected
"""

import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "YOUR_APP_PASSWORD"


def send_alert(recipient, risk_level):
    msg = EmailMessage()
    msg["Subject"] = "[ALERT] Possible Wi-Fi Deauthentication Attack"
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient

    msg.set_content(f"""
A potential Wi-Fi attack has been detected.

Risk Level: {risk_level}

Recommended Actions:
- Change Wi-Fi password
- Enable WPA3 / Protected Management Frames (PMF)
- Disable WPS
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
