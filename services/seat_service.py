from typing import Optional, List
from models.seat import Seat
from repositories.seat_repo import SeatRepo
from sqlalchemy.orm import Session


class SeatService:
    def __init__(self):
        self.seat_repo = SeatRepo()

    def get_seats_by_plane(self, session: Session, plane_id: int) -> List[Seat]:
        return self.seat_repo.get_seats_by_plane_id(session, plane_id)

    def get_seat_by_id(self, session: Session, seat_id: int) -> Optional[Seat]:
        seat = self.seat_repo.get_seat_by_id(session, seat_id)
        if not seat:
            raise ValueError("Seat not found")
        return seat

    def get_available_seats(self, session: Session, flight_id: int, plane_id: int) -> List[Seat]:
        return self.seat_repo.get_available_seats_per_flight(session, flight_id, plane_id)

    def get_available_seats_count(self, session: Session, flight_id: int, plane_id: int) -> int:
        return self.seat_repo.get_available_seats_count(session, flight_id, plane_id)