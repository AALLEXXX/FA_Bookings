from fastapi import APIRouter, Depends
from app.hotels.rooms.schemas import SRoomsSearchArgs

from app.hotels.rooms.dao import RoomDAO

router = APIRouter(prefix="/hotels",
                   tags=['Комнаты'])


@router.get("/{hotel_id}/rooms")
async def get_rooms(body: SRoomsSearchArgs = Depends()):
    result = await RoomDAO.find_all(body.hotel_id,
                               date_to=body.date_to,
                                 date_from=body.date_from)
    return result



