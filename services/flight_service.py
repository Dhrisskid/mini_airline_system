from datetime import date, time
from typing import Optional, List
from models.flight import Flight, FlightStatus
from repositories.flight_repo import FlightRepo
from repositories.plane_repo import PlaneRepo
from sqlalchemy.orm import Session


class FlightService:
    def __init__(self):
        self.flight_repo = FlightRepo()
        self.plane_repo = PlaneRepo()

    def _generate_flight_code(self, session: Session, origin: str, destination: str) -> str:
        prefix = f"{origin[:2].upper()}{destination[:2].upper()}"
        all_flights = self.flight_repo.get_all(session)
        same_route = [f for f in all_flights
                      if f.origin.upper() == origin.upper()
                      and f.destination.upper() == destination.upper()]
        sequence = len(same_route) + 1
        return f"{prefix}{sequence:03d}"

    def create_flight(self, session: Session, plane_id: int, origin: str, destination: str,
                      flight_date: date, departure_time: time, price_per_seat: float) -> Optional[Flight]:
        if not self.plane_repo.get_by_id(session, plane_id):
            raise ValueError("Plane not found")
        flight_code = self._generate_flight_code(session, origin, destination)
        new_flight = Flight(
            plane_id=plane_id,
            origin=origin,
            destination=destination,
            date=flight_date,
            departure_time=departure_time,
            price_per_seat=price_per_seat,
            flight_code=flight_code
        )
        try:
            return self.flight_repo.create(session, new_flight)
        except Exception:
            raise ValueError("Failed to create flight")

    def get_flight_by_id(self, session: Session, flight_id: int) -> Optional[Flight]:
        flight = self.flight_repo.get_by_id(session, flight_id)
        if not flight:
            raise ValueError("Flight not found")
        return flight

    def get_flight_by_code(self, session: Session, flight_code: str) -> Optional[Flight]:
        flight = self.flight_repo.get_by_flight_code(session, flight_code)
        if not flight:
            raise ValueError("Flight not found")
        return flight

    def get_all_flights(self, session: Session) -> List[Flight]:
        return self.flight_repo.get_all(session)

    def get_available_flights(self, session: Session) -> List[Flight]:
        return self.flight_repo.get_available(session)

    def search_by_origin(self, session: Session, origin: str) -> List[Flight]:
        return self.flight_repo.search_by_origin(session, origin)

    def search_by_destination(self, session: Session, destination: str) -> List[Flight]:
        return self.flight_repo.search_by_destination(session, destination)

    def search_by_date(self, session: Session, flight_date: date) -> List[Flight]:
        return self.flight_repo.search_by_date(session, flight_date)

    def search_flights(self, session: Session, origin: str, destination: str, flight_date: date) -> List[Flight]:
        return self.flight_repo.search(session, origin, destination, flight_date)

    def update_flight_status(self, session: Session, flight_id: int, status: FlightStatus) -> Optional[Flight]:
        if not self.flight_repo.get_by_id(session, flight_id):
            raise ValueError("Flight not found")
        try:
            return self.flight_repo.update_status(session, flight_id, status)
        except Exception:
            raise ValueError("Failed to update flight status")

    def update_flight_price(self, session: Session, flight_id: int, price: float) -> Optional[Flight]:
        if not self.flight_repo.get_by_id(session, flight_id):
            raise ValueError("Flight not found")
        try:
            return self.flight_repo.update_price(session, flight_id, price)
        except Exception:
            raise ValueError("Failed to update flight price")


