import re
from pydantic import BaseModel, Field, field_validator


class Booking(BaseModel):
    movie_name: str
    seats: int = Field(gt=0)
    show_time: str

    @field_validator("show_time")
    @classmethod
    def validate_show_time(cls, value: str) -> str:
        if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", value):
            raise ValueError("show_time must be in HH:MM format (24-hour clock)")
        return value
