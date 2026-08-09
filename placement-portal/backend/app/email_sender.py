import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app


def send_email(
    recipient,
    subject,
    html_content
):

    sender = current_app.config["MAIL_USERNAME"]
    password = current_app.config["MAIL_PASSWORD"]

    message = MIMEMultipart("alternative")

    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient

    html_part = MIMEText(
        html_content,
        "html",
        "utf-8"
    )

    message.attach(html_part)

    with smtplib.SMTP(
        current_app.config["MAIL_SERVER"],
        current_app.config["MAIL_PORT"]
    ) as server:

        server.starttls()

        server.login(
            sender,
            password
        )

        server.sendmail(
            sender,
            recipient,
            message.as_string()
        )