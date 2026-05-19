from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from persistence.dB import get_db
from services.seat_service import SeatService
from schemas.responses.seat_response import SeatResponse

router = APIRouter(prefix="/seats", tags=["Seats"])
seat_service = SeatService()


@router.get("/plane/{plane_id}", response_model=List[SeatResponse])
def get_seats_by_plane(plane_id: int, db: Session = Depends(get_db)):
    return seat_service.get_seats_by_plane(db, plane_id)


@router.get("/available/{flight_id}", response_model=List[SeatResponse])
def get_available_seats(flight_id: int, plane_id: int, db: Session = Depends(get_db)):
    return seat_service.get_available_seats(db, flight_id, plane_id)


@router.get("/available/{flight_id}/count")
def get_available_seats_count(flight_id: int, plane_id: int, db: Session = Depends(get_db)):
    return {"available_seats": seat_service.get_available_seats_count(db, flight_id, plane_id)}


@router.get("/{seat_id}", response_model=SeatResponse)
def get_seat(seat_id: int, db: Session = Depends(get_db)):
    try:
        return seat_service.get_seat_by_id(db, seat_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))