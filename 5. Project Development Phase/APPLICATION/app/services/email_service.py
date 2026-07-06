import os
import smtplib
from email.message import EmailMessage
import logging

logger = logging.getLogger(__name__)


def _get_smtp_config():
    return {
        "host": os.getenv("EMAIL_HOST"),
        "port": int(os.getenv("EMAIL_PORT", "587")),
        "user": os.getenv("EMAIL_HOST_USER"),
        "password": os.getenv("EMAIL_HOST_PASSWORD"),
        "sender": os.getenv("EMAIL_FROM", os.getenv("EMAIL_HOST_USER")),
    }


def send_email(to_email: str, subject: str, body: str, html: str | None = None) -> None:
    cfg = _get_smtp_config()
    if not cfg["host"] or not cfg["user"] or not cfg["password"]:
        logger.info("SMTP configuration not found; skipping email send")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = cfg["sender"]
    msg["To"] = to_email
    if html:
        msg.set_content(body)
        msg.add_alternative(html, subtype="html")
    else:
        msg.set_content(body)

    try:
        if cfg["port"] == 465:
            with smtplib.SMTP_SSL(cfg["host"], cfg["port"]) as smtp:
                smtp.login(cfg["user"], cfg["password"])
                smtp.send_message(msg)
        else:
            with smtplib.SMTP(cfg["host"], cfg["port"]) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(cfg["user"], cfg["password"])
                smtp.send_message(msg)
        logger.info(f"Email sent to %s", to_email)
    except Exception as e:
        logger.exception("Failed to send email to %s: %s", to_email, e)


def send_registration_email(to_email: str, name: str | None = None) -> None:
    subject = "FinRelief AI — Registration Successful"
    body = f"Hi {name or ''},\n\nThank you for registering at FinRelief AI. Your account has been created successfully.\n\nBest,\nFinRelief AI Team"
    html = f"""
    <p>Hi {name or ''},</p>
    <p>Thank you for registering at <strong>FinRelief AI</strong>. Your account has been created successfully.</p>
    <p>Best,<br/>FinRelief AI Team</p>
    """
    send_email(to_email, subject, body, html)


def send_login_notification(to_email: str, name: str | None = None) -> None:
    subject = "FinRelief AI — Login Notification"
    body = f"Hi {name or ''},\n\nYou have successfully logged in to FinRelief AI. If this wasn't you, please secure your account.\n\nBest,\nFinRelief AI Team"
    html = f"""
    <p>Hi {name or ''},</p>
    <p>You have successfully logged in to <strong>FinRelief AI</strong>. If this wasn't you, please secure your account immediately.</p>
    <p>Best,<br/>FinRelief AI Team</p>
    """
    send_email(to_email, subject, body, html)
