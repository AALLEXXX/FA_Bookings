import asyncio

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.schemas import HotelSearchArgs

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}")
@cache(expire=20)
async def get_hotels(search_args: HotelSearchArgs = Depends()):
    await asyncio.sleep(10)
    result = await HotelDAO.find_all(
        search_args.location, search_args.date_from, search_args.date_to
    )
    return result
