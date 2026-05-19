from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from persistence.dB import get_db
from services.passenger_service import PassengerService
from schemas.requests.passenger_request import UpdatePassengerRequest
from schemas.responses.passenger_response import PassengerResponse

router = APIRouter(prefix="/passengers", tags=["Passengers"])
passenger_service = PassengerService()


@router.get("/user/{user_id}", response_model=PassengerResponse)
def get_passenger_by_user_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return passenger_service.get_passenger_by_user_id(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/email/{email}", response_model=PassengerResponse)
def get_passenger_by_email(email: str, db: Session = Depends(get_db)):
    try:
        return passenger_service.get_passenger_by_email(db, email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{passenger_id}", response_model=PassengerResponse)
def get_passenger(passenger_id: int, db: Session = Depends(get_db)):
    try:
        return passenger_service.get_passenger_by_id(db, passenger_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{passenger_id}", response_model=PassengerResponse)
def update_passenger(passenger_id: int, body: UpdatePassengerRequest, db: Session = Depends(get_db)):
    try:
        return passenger_service.update_details(db, passenger_id, name=body.name, phone=body.phone)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))