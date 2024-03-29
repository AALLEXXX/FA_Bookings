from dataclasses import dataclass
from datetime import date
from typing import List

from fastapi import Query
from pydantic import BaseModel


@dataclass
class HotelSearchArgs:
    location: str
    date_from: date
    date_to: date
    has_spa: bool = None
    stars: int = Query(None, ge=1, le=5)

class SHotelAndRooms(BaseModel):
    hotel_id: int
    name: str
    location: str
    services: List[str]
    image_id: int 
    total_rooms: int 
    available_rooms: int 