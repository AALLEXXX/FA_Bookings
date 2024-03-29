from datetime import date
from typing import List

from pydantic import BaseModel


class SRoomsSearchArgs(BaseModel):
    hotel_id: int
    date_from: date
    date_to: date


class SGetRooms(BaseModel):
    hotel_id: int
    room_name: str
    description: str
    services: List[List]
    price: int
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int
    