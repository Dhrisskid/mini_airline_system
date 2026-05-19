from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from persistence.dB import get_db
from services.booking_service import BookingService
from schemas.requests.booking_request import BookingRequestModel, CancelBookingRequest
from schemas.responses.booking_response import BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])
booking_service = BookingService()


@router.post("/", response_model=BookingResponse, status_code=201)
def book_flight(body: BookingRequestModel, db: Session = Depends(get_db)):
    try:
        return booking_service.book_flight(
            db,
            body.user_id,
            body.name,
            body.phone,
            body.flight_id,
            body.seat_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(booking_id: int, body: CancelBookingRequest, db: Session = Depends(get_db)):
    try:
        return booking_service.cancel_booking(db, booking_id, body.cancelled_by_airline)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pnr/{pnr}", response_model=BookingResponse)
def get_booking_by_pnr(pnr: str, db: Session = Depends(get_db)):
    try:
        return booking_service.get_booking_by_pnr(db, pnr)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/passenger/{passenger_id}", response_model=List[BookingResponse])
def get_bookings_by_passenger(passenger_id: int, db: Session = Depends(get_db)):
    try:
        return booking_service.get_bookings_by_passenger(db, passenger_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/flight/{flight_id}/active", response_model=List[BookingResponse])
def get_active_bookings_by_flight(flight_id: int, db: Session = Depends(get_db)):
    try:
        return booking_service.get_active_bookings_per_flight(db, flight_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/flight/{flight_id}", response_model=List[BookingResponse])
def get_bookings_by_flight(flight_id: int, db: Session = Depends(get_db)):
    try:
        return booking_service.get_bookings_by_flight(db, flight_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        return booking_service.get_booking_by_id(db, booking_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))