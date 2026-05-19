from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.booking import Booking, BookingStatus


class BookRepo:
    def create(self, session: Session, booking: Booking) -> Optional[Booking]:
        try:
            session.add(booking)
            session.flush()
            return booking
        except Exception as e:
            session.rollback()
            raise e

    def get_by_id(self, session: Session, id: int) -> Optional[Booking]:
        try:
            bk = select(Booking).where(Booking.id == id)
            booking = session.scalar(bk)
            return booking
        except Exception as e:
            raise e

    def get_by_pnr(self, session: Session, pnr: str) -> Optional[Booking]:
        try:
            bk = select(Booking).where(Booking.pnr == pnr)
            booking = session.scalar(bk)
            return booking
        except Exception as e:
            raise e

    def get_by_passenger_id(self, session: Session, passenger_id: int) -> List[Booking]:
        try:
            bk = select(Booking).where(Booking.passenger_id == passenger_id)
            booking = session.scalars(bk).all()
            return booking
        except Exception as e:
            raise e

    def get_by_flight_id(self, session: Session, flight_id: int) -> List[Booking]:
        try:
            bk = select(Booking).where(Booking.flight_id == flight_id)
            booking = session.scalars(bk).all()
            return booking
        except Exception as e:
            raise e

    def check_booking(self, session: Session, seat_id: int, flight_id: int) -> Optional[Booking]:
        try:
            bk = select(Booking).where(Booking.seat_id == seat_id, Booking.flight_id == flight_id)
            booking = session.scalar(bk)
            return booking
        except Exception as e:
            raise e

    def update_booking(self, session: Session, id: int, status: BookingStatus) -> Optional[Booking]:
        try:
            bk = select(Booking).where(Booking.id == id)
            booking = session.scalar(bk)
            if booking:
                booking.booking_status = status
                session.flush()
            return booking
        except Exception as e:
            session.rollback()
            raise e

    def active_bookings_per_flight(self, session: Session, flight_id: int) -> List[Booking]:
        try:
            bk = select(Booking).where(Booking.flight_id == flight_id, Booking.booking_status == BookingStatus.active)
            booking = session.scalars(bk).all()
            return booking
        except Exception as e:
            raise e
