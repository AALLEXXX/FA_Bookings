from app.schemas.hotels import HotelSearchArgs
from app.utils.repository import AbstractRepository


class HotelsService:
    def __init__(self, hotels_repo: AbstractRepository) -> None:
        self.hotels_repo = hotels_repo

    async def get_hotels(self, search_args: HotelSearchArgs):
        result = await self.hotels_repo.find_all(
            search_args.location, search_args.date_from, search_args.date_to
        )
        #TODO сделать дамп
        return result
