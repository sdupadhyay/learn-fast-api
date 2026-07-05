from fastapi import Query
from typing import List
from schemas.booking_schema import Booking
from fastapi import APIRouter

router = APIRouter(prefix="/booking", tags=["booking"])


@router.post("/create/{city_name}")
def create_ticket(city_name: str, booking_details: Booking, hall: str):
    return {
        "city": city_name,
        "hall": hall,
        "movie": booking_details.movie_name,
        "seats": booking_details.seats,
        "time": booking_details.show_time,
        "message": "Booking confirmed!",
    }


@router.get("/snacks")
def get_snacks(snacks: List[str] = Query(...)):
    return {"selected_snacks": snacks}
