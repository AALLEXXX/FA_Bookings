from abc import ABC, abstractmethod

from sqlalchemy import Result, ResultProxy, insert, select

from app.database import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add(): 
        raise NotImplementedError
    
    @abstractmethod
    async def find_all(): 
        raise NotImplementedError
    
    @abstractmethod
    async def find_by_id(): 
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_none(): 
        raise NotImplementedError

class SQLAlchemyRepository(AbstractRepository):
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.id == model_id)
            result: ResultProxy = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result: ResultProxy = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result: Result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model.__table__).values(**data)
            await session.execute(query)
            await session.commit()
