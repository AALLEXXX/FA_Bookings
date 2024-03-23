from datetime import date, timedelta
from datetime import datetime
from app.exeptions import IncorrectDateForBooking


def validate_date(room_id, date_from: date, date_to: date): #TODO
    
    if date_from > date_to:
        raise IncorrectDateForBooking(
            "Дата начала бронирования не может быть позже даты окончания"
        )

    if date_from < datetime.now().date():
        raise IncorrectDateForBooking(
            "Дата начала бронирования не может быть раньше текущей даты"
        )

    max_booking_duration = timedelta(days=30)
    if date_to > date_from + max_booking_duration:
        raise IncorrectDateForBooking(
            "Продолжительность бранирования не может превышать один месяц"
        )

    if date_from > datetime.now().date() + max_booking_duration:
        raise IncorrectDateForBooking(
            "Дата бронирования не может быть больше текущей даты на 30 дней"
        )