from datetime import date
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.flight import Flight, FlightStatus


class FlightRepo:
    def create(self, session: Session, flight: Flight) -> Flight:
        try:
            session.add(flight)
            session.flush()
            return flight
        except Exception as e:
            session.rollback()
            raise e

    def get_by_id(self, session: Session, flight_id: int) -> Optional[Flight]:
        try:
            flt = select(Flight).where(Flight.id == flight_id)
            flight = session.scalar(flt)
            return flight
        except Exception as e:
            raise e

    def get_by_flight_code(self, session: Session, flight_code: str) -> Optional[Flight]:
        try:
            flt = select(Flight).where(Flight.flight_code == flight_code)
            flight = session.scalar(flt)
            return flight
        except Exception as e:
            raise e

    def get_all(self, session: Session) -> List[Flight]:
        try:
            flt = select(Flight).order_by(Flight.id.desc())
            flights = session.scalars(flt).all()
            return flights
        except Exception as e:
            raise e

    def get_available(self, session: Session) -> List[Flight]:
        try:
            available = [a for a in self.get_all(session) if a.status != FlightStatus.landed and a.status != FlightStatus.cancelled]
            return available
        except Exception as e:
            raise e

    def search_by_origin(self, session: Session, origin: str) -> List[Flight]:
        try:
            flt = select(Flight).where(Flight.origin.ilike(f'%{origin}%'))
            flights = session.scalars(flt).all()
            return flights
        except Exception as e:
            raise e

    def search_by_destination(self, session: Session, destination: str) -> List[Flight]:
        try:
            flt = select(Flight).where(Flight.destination.ilike(f'%{destination}%'))
            flights = session.scalars(flt).all()
            return flights

        except Exception as e:
            raise e

    def search_by_date(self, session: Session, date: date) -> List[Flight]:
        try:
            flt = select(Flight).where(Flight.date == date)
            flights = session.scalars(flt).all()
            return flights
        except Exception as e:
            raise e

    def search(self, session: Session, origin: str, destination: str, date: date) -> List[Flight]:
        try:
            flt = (select(Flight).where(
                    Flight.origin.ilike(f'%{origin}%'),
                    Flight.destination.ilike(f'%{destination}%'),
                    Flight.date == date))
            flights = session.scalars(flt).all()
            return flights
        except Exception as e:
            raise e

    def update_status(self, session: Session, flight_id: int, status: FlightStatus) -> Optional[Flight]:
        try:
            flt = select(Flight).where(Flight.id == flight_id)
            flight = session.scalar(flt)
            if flight:
                flight.status = status
                session.flush()
            return flight
        except Exception as e:
            session.rollback()
            raise e

    def update_price(self, session: Session, flight_id: int, price: float) -> Optional[Flight]:
        try:
            flt = select(Flight).where(Flight.id == flight_id)
            flight = session.scalar(flt)
            if flight:
                flight.price_per_seat = price
                session.flush()
            return flight
        except Exception as e:
            session.rollback()
            raise e


