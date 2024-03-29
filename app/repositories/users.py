from app.utils.repository import SQLAlchemyRepository
from app.models.users import Users


class UserRepository(SQLAlchemyRepository):
    model = Users
