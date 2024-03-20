from app.dao.base import BaseDAO
from app.users.user_model import Users


class UserDAO(BaseDAO):
    model = Users
