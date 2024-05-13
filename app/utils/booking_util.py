from datetime import date, timedelta
from datetime import datetime
from app.exeptions import IncorrectDate


def validate_date(date_from: date, date_to: date): #qweTODOeqe
    print(type(date_to))
    # if date_to is not date:
    #     raise IncorrectDate(
    #         "Некорректный формат даты"
    #     )
    if not isinstance(date_to, date):
        raise IncorrectDate(
            "Некорректный формат даты"
        )
    if date_from > date_to:
        raise IncorrectDate(
            "Дата начала не может быть позже даты окончания"
        )

    if date_from < datetime.now().date():
        raise IncorrectDate(
            "Дата начала не может быть раньше текущей даты"
        )

    max_booking_duration = timedelta(days=30)
    if date_to > date_from + max_booking_duration:
        raise IncorrectDate(
            "Продолжительность не может превышать один месяц"
        )

    if date_from > datetime.now().date() + max_booking_duration:
        raise IncorrectDate(
            "Дата не может быть больше текущей даты на 30 дней"
        )