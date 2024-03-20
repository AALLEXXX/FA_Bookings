from dataclasses import dataclass
from datetime import date

from fastapi import Query


@dataclass
class HotelSearchArgs:
    location: str
    date_from: date
    date_to: date
    has_spa: bool = None
    stars: int = Query(None, ge=1, le=5)
