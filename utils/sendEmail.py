from fastapi import  HTTPException
from email.message import EmailMessage
import smtplib


def sendEmail(fromEmailAddress, toEmailAddress, emailAppKey):
    msg = EmailMessage()
    msg["Subject"] = "We got your interest!"
    msg["From"] = fromEmailAddress
    msg["To"] = toEmailAddress# replace with recipient once you make it good :)

    with open("email_template.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(fromEmailAddress, emailAppKey)
            smtp.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")