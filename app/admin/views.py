from sqladmin import ModelView

from app.models.hotels import Hotels

from ..models.bookings import Bookings
from ..models.rooms import Rooms
from ..models.users import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_list += [Users.bookings]
    can_delete = False
    column_details_exclude_list = [Users.hashed_password]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Hotels.__table__.c]
    can_delete = False
    column_details_exclude_list = [Rooms.id]
    name = "Команата"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c]
    column_details_exclude_list = [Hotels.id]

    can_delete = False
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]
    column_details_exclude_list = [Bookings.id]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"
