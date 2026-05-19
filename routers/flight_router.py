from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from persistence.dB import get_db
from services.flight_service import FlightService
from schemas.requests.flight_request import CreateFlightRequest, UpdateFlightStatusRequest, UpdateFlightPriceRequest
from schemas.responses.flight_response import FlightResponse

router = APIRouter(prefix="/flights", tags=["Flights"])
flight_service = FlightService()


@router.post("/", response_model=FlightResponse, status_code=201)
def create_flight(body: CreateFlightRequest, db: Session = Depends(get_db)):
    try:
        return flight_service.create_flight(
            db,
            body.plane_id,
            body.origin,
            body.destination,
            body.date,
            body.departure_time,
            body.price_per_seat
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/available", response_model=List[FlightResponse])
def get_available_flights(db: Session = Depends(get_db)):
    return flight_service.get_available_flights(db)


@router.get("/search", response_model=List[FlightResponse])
def search_flights(origin: str, destination: str, flight_date: date, db: Session = Depends(get_db)):
    return flight_service.search_flights(db, origin, destination, flight_date)


@router.get("/search/origin", response_model=List[FlightResponse])
def search_by_origin(origin: str, db: Session = Depends(get_db)):
    return flight_service.search_by_origin(db, origin)


@router.get("/search/destination", response_model=List[FlightResponse])
def search_by_destination(destination: str, db: Session = Depends(get_db)):
    return flight_service.search_by_destination(db, destination)


@router.get("/search/date", response_model=List[FlightResponse])
def search_by_date(flight_date: date, db: Session = Depends(get_db)):
    return flight_service.search_by_date(db, flight_date)


@router.get("/code/{flight_code}", response_model=FlightResponse)
def get_flight_by_code(flight_code: str, db: Session = Depends(get_db)):
    try:
        return flight_service.get_flight_by_code(db, flight_code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[FlightResponse])
def get_all_flights(db: Session = Depends(get_db)):
    return flight_service.get_all_flights(db)


@router.get("/{flight_id}", response_model=FlightResponse)
def get_flight(flight_id: int, db: Session = Depends(get_db)):
    try:
        return flight_service.get_flight_by_id(db, flight_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{flight_id}/status", response_model=FlightResponse)
def update_status(flight_id: int, body: UpdateFlightStatusRequest, db: Session = Depends(get_db)):
    try:
        return flight_service.update_flight_status(db, flight_id, body.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{flight_id}/price", response_model=FlightResponse)
def update_price(flight_id: int, body: UpdateFlightPriceRequest, db: Session = Depends(get_db)):
    try:
        return flight_service.update_flight_price(db, flight_id, body.price)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))