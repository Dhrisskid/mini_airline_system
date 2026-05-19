from typing import Optional, List
from models.plane import Plane
from models.seat import Seat
from repositories.plane_repo import PlaneRepo
from repositories.seat_repo import SeatRepo
from sqlalchemy.orm import Session


class PlaneService:
    def __init__(self):
        self.plane_repo = PlaneRepo()
        self.seat_repo = SeatRepo()

    def _generate_seats(self, total_seats: int, plane_id: int) -> List[Seat]:
        seats = []
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        count = 0
        for letter in letters:
            for number in range(1, 7):
                if count >= total_seats:
                    return seats
                seats.append(Seat(plane_id=plane_id, seat_no=f"{letter}{number}"))
                count += 1
        return seats

    def create_plane(self, session: Session, model: str, total_seats: int) -> Optional[Plane]:
        if total_seats <= 0:
            raise ValueError("Total seats must be greater than zero")
        if total_seats > 156:
            raise ValueError("Total seats cannot exceed 156")
        new_plane = Plane(model=model, total_seats=total_seats)
        try:
            created_plane = self.plane_repo.create(session, new_plane)
            seats = self._generate_seats(total_seats, created_plane.id)
            self.seat_repo.add(session, seats)
            return created_plane
        except Exception:
            raise ValueError("Failed to create plane")

    def get_plane_by_id(self, session: Session, plane_id: int) -> Optional[Plane]:
        plane = self.plane_repo.get_by_id(session, plane_id)
        if not plane:
            raise ValueError("Plane not found")
        return plane

    def get_all_planes(self, session: Session) -> List[Plane]:
        return self.plane_repo.get_all(session)

    def delete_plane(self, session: Session, plane_id: int) -> Optional[Plane]:
        if not self.plane_repo.get_by_id(session, plane_id):
            raise ValueError("Plane not found")
        try:
            return self.plane_repo.delete(session, plane_id)
        except Exception:
            raise ValueError("Failed to delete plane")


        