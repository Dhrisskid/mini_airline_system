from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.booking import BookingStatus, Booking
from models.seat import Seat


class SeatRepo:
    def add(self, session: Session, seats: List[Seat]) -> List[Seat]:
        try:
            session.add_all(seats)
            session.flush()
            return seats
        except Exception as e:
            session.rollback()
            raise e

    def get_seats_by_plane_id(self, session: Session, plane_id: int) -> List[Seat]:
        try:
            st = select(Seat).where(Seat.plane_id == plane_id)
            return session.scalars(st).all()
        except Exception as e:
            raise e

    def get_seat_by_id(self, session: Session, seat_id: int) -> Optional[Seat]:
        try:
            st = select(Seat).where(Seat.id == seat_id)
            return session.scalar(st)
        except Exception as e:
            raise e

    def get_available_seats_per_flight(self, session: Session, flight_id: int, plane_id: int) -> List[Seat]:
        try:
            st = select(Seat).where(Seat.plane_id == plane_id)
            seats = session.scalars(st).all()
            bk = select(Booking).where(
                Booking.flight_id == flight_id,
                Booking.booking_status == BookingStatus.active)
            bookings = session.scalars(bk).all()
            booked_seat_ids = {booking.seat_id for booking in bookings}
            return [seat for seat in seats if seat.id not in booked_seat_ids]
        except Exception as e:
            raise e

    def get_available_seats_count(self, session: Session, flight_id: int, plane_id: int) -> int:
        try:
            return len(self.get_available_seats_per_flight(session, flight_id, plane_id))
        except Exception as e:
            raise e










