from datetime import date

from pydantic import BaseModel


class SRoomsSearchArgs(BaseModel):
    hotel_id: int 
    date_from: date
    date_to: date

