import asyncio
from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.schemas import HotelSearchArgs, SHotelAndRooms
from app.utils.booking_util import validate_date

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}", dependencies=[Depends(validate_date)])
@cache(expire=20)
async def get_hotels(search_args: HotelSearchArgs = Depends()) -> List[SHotelAndRooms]:
    result = await HotelDAO.find_all(
        search_args.location, search_args.date_from, search_args.date_to
    )

    return result
