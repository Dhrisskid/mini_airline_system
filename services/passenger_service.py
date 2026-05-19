from typing import Optional
from models.passenger import Passenger
from repositories.passenger_repo import PassengerRepo
from sqlalchemy.orm import Session


class PassengerService:
    def __init__(self):
        self.passenger_repo = PassengerRepo()

    def get_passenger_by_id(self, session: Session, passenger_id: int) -> Optional[Passenger]:
        passenger = self.passenger_repo.get_by_id(session, passenger_id)
        if not passenger:
            raise ValueError("Passenger not found")
        return passenger

    def get_passenger_by_user_id(self, session: Session, user_id: int) -> Optional[Passenger]:
        passenger = self.passenger_repo.get_by_user_id(session, user_id)
        if not passenger:
            raise ValueError("Passenger not found")
        return passenger

    def get_passenger_by_email(self, session: Session, email: str) -> Optional[Passenger]:
        passenger = self.passenger_repo.get_by_email(session, email)
        if not passenger:
            raise ValueError("Passenger not found")
        return passenger

    def update_details(self, session: Session, passenger_id: int, name: str = None, phone: str = None) -> Optional[Passenger]:
        passenger = self.passenger_repo.get_by_id(session, passenger_id)
        if not passenger:
            raise ValueError("Passenger not found")
        try:
            return self.passenger_repo.update_details(session, passenger_id, name=name, phone=phone)
        except Exception:
            raise ValueError("Failed to update passenger details")