from typing import List
from fastapi import APIRouter, Depends

from app.api.dependencies import get_rooms_service
from app.schemas.rooms import SGetRooms, SRoomsSearchArgs
from app.services.rooms import RoomsService

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(room: SRoomsSearchArgs = Depends(),
                    rooms_service: RoomsService = Depends(get_rooms_service)
                    ) -> List[SGetRooms]:
    return await rooms_service.get_rooms(room=room)
