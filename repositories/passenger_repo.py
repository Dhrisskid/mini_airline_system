from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.passenger import Passenger


class PassengerRepo:
    def create(self, session: Session, passenger: Passenger) -> Optional[Passenger]:
        try:
            session.add(passenger)
            session.flush()
            return passenger
        except Exception as e:
            session.rollback()
            raise e

    def get_by_id(self, session: Session, id: int) -> Optional[Passenger]:
        try:
            ps = select(Passenger).where(Passenger.id == id)
            return session.scalar(ps)
        except Exception as e:
            raise e

    def get_by_user_id(self, session: Session, user_id: int) -> Optional[Passenger]:
        try:
            ps = select(Passenger).where(Passenger.user_id == user_id)
            return session.scalar(ps)
        except Exception as e:
            raise e

    def get_by_email(self, session: Session, email: str) -> Optional[Passenger]:
        try:
            ps = select(Passenger).where(Passenger.email == email)
            return session.scalar(ps)
        except Exception as e:
            raise e

    def update_details(self, session: Session, id: int, name: str = None, phone: str = None) -> Optional[Passenger]:
        try:
            ps = select(Passenger).where(Passenger.id == id)
            passenger = session.scalar(ps)
            if passenger:
                if name:
                    passenger.name = name
                if phone:
                    passenger.phone = phone
                session.flush()
            return passenger
        except Exception as e:
            session.rollback()
            raise e


        
