from datetime import date
from email.message import EmailMessage
from pydantic import EmailStr
from app.config import settings

def create_booking_confirmation_template(
    booking: dict,
    email_to: EmailStr
):
    
    email = EmailMessage()
    email['Subject'] = 'Подтверждение бронирования'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to

    email.set_content(
        f"""
            <h1> Подтвердите бронирование </h1>
            Вы забронировали отель с {booking['date_from']} по {booking['date_to']}
        """,
        subtype='html'
    )

    return email



def plural_days(n: int) -> str:
    days = ['день', 'дня', 'дней']
    
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]


def create_booking_reminder_template(
    date_from: date,
    date_to: date,
    email_to: EmailStr,
    days: int,
):
    email = EmailMessage()

    days_str = plural_days(days)
    email["Subject"] = f"Осталось {days_str} до заселения"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Напоминание о бронировании</h1>
            Вы забронировали отель с {date_from} по {date_to}
        """,
        subtype="html"
    )
    return email