from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.api.dependencies import get_hotels_service
from app.schemas.hotels import HotelSearchArgs, SHotelAndRooms
from app.services.hotels import HotelsService
from app.utils.booking_util import validate_date

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}", dependencies=[Depends(validate_date)])
@cache(expire=20)
async def get_hotels(search_args: HotelSearchArgs = Depends(),
                     hotel_service: HotelsService = Depends(get_hotels_service)
                     ) -> List[SHotelAndRooms]:
    return await hotel_service.get_hotels(search_args=search_args)
