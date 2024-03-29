from app.utils.repository import AbstractRepository


class RoomsService:
    def __init__(self, rooms_repo: AbstractRepository) -> None:
        self.rooms_repo = rooms_repo

    async def get_rooms(self, room):
        result = await self.rooms_repo.find_all(
        room.hotel_id, date_to=room.date_to, date_from=room.date_from)
        return result

