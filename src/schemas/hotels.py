from pydantic import BaseModel


class Hotel(BaseModel):
    title: str
    name: str


class HotelPatch(BaseModel):
    title: str | None
    name: str | None