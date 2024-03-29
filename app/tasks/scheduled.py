import asyncio
import smtplib
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.config import settings
from app.database import async_session_nullpool
from app.logger import logger
from app.tasks.celery_conf import celery_app
from app.tasks.email_templates import create_booking_reminder_template
from app.users.models import Users


async def get_users_email_and_dates(days: int) -> list[dict | None] | None:
    try:
        query = (
            select(Users.email, Bookings.date_from, Bookings.date_to)
            .select_from(Users)
            .join(Bookings, Users.id == Bookings.user_id)
            .filter(Bookings.date_from - timedelta(days=days) == date.today())
        )

        async with async_session_nullpool() as session:
            result = await session.execute(query)
            return result.mappings().all()
    except (SQLAlchemyError, Exception):
        logger.error("An error occurred in get_users_email_and_dates", exc_info=True)
        return None


async def remind_of_booking(days: int) -> None:
    try:
        if bookings := await get_users_email_and_dates(days):

            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASS)

                for booking in bookings:
                    email_to = booking["email"]

                    if settings.MODE == "DEV":
                        email_to = settings.SMTP_USER

                    date_to = (booking["date_from"],)
                    date_from = booking["date_from"]

                    msg = create_booking_reminder_template(
                        date_from, date_to, email_to, days
                    )

                    server.send_message(msg)
    except Exception:
        logger.error("An error occurred in remind_of_booking", exc_info=True)


@celery_app.task(name="email.booking_reminder_1day")
def remind_booking_1day(days: int = 1):
    asyncio.run(remind_of_booking(days))


@celery_app.task(name="email.booking_reminder_3day")
def remind_booking_3days(days: int = 3):
    asyncio.run(remind_of_booking(days))
