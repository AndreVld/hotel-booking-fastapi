import smtplib

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_conf import celery_app
from app.tasks.email_templates import create_booking_confirmation_template


@celery_app.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):

    if settings.MODE == "DEV":
        email_to = settings.SMTP_USER

    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
