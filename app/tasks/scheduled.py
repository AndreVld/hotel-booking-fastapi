from datetime import date, timedelta
import smtplib
from sqlalchemy import select
from app.bookings.models import Bookings
from app.tasks.celery_conf import celery_app
from app.tasks.email_templates import create_booking_reminder_template
from app.users.models import Users
from app.database import async_session_nullpool
from app.config import settings
import asyncio



async def get_users_email_and_dates(days: int)->list[dict | None]: 

    query = (
        select(Users.email, Bookings.date_from, Bookings.date_to)
        .select_from(Users)
        .join(Bookings, Users.id==Bookings.user_id)
        .filter(Bookings.date_from - timedelta(days=days) == date.today())
    )
    
    async with async_session_nullpool() as session:
        result = await session.execute(query)
        return result.mappings().all()
        

async def remind_of_booking(days:int):
    if bookings:= await get_users_email_and_dates(days):

        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)

            for booking in bookings:
                # email_to = booking['email']
                email_to = settings.SMTP_USER

                date_to = booking['date_from'],
                date_from = booking['date_from']

                msg = create_booking_reminder_template(date_from, date_to, email_to, days)
                
                server.send_message(msg)

@celery_app.task(name='email.booking_reminder_1day')
def remind_booking_1day(days: int = 1):
    asyncio.run(remind_of_booking(days))

@celery_app.task(name='email.booking_reminder_3day')
def remind_booking_3days(days: int = 3):
    asyncio.run(remind_of_booking(days))
