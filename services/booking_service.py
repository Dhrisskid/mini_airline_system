import random
import string
from typing import Optional, List
from models.booking import Booking, BookingStatus
from models.flight import FlightStatus
from models.passenger import Passenger
from repositories.booking_repo import BookRepo
from repositories.flight_repo import FlightRepo
from repositories.passenger_repo import PassengerRepo
from repositories.seat_repo import SeatRepo
from repositories.user_repo import UserRepo
from sqlalchemy.orm import Session


class BookingService:
    def __init__(self):
        self.booking_repo = BookRepo()
        self.flight_repo = FlightRepo()
        self.passenger_repo = PassengerRepo()
        self.seat_repo = SeatRepo()
        self.user_repo = UserRepo()

    def generate_pnr(self) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def get_or_create_passenger(self, session: Session, user_id: int, name: str, phone: str) -> Passenger:
        passenger = self.passenger_repo.get_by_user_id(session, user_id)
        if not passenger:
            user = self.user_repo.get_by_id(session, user_id)
            if not user:
                raise ValueError("User not found")
            new_passenger = Passenger(name=name, phone=phone, email=user.email, user_id=user_id)
            passenger = self.passenger_repo.create(session, new_passenger)
        return passenger

    def book_flight(self, session: Session, user_id: int, name: str, phone: str, flight_id: int, seat_id: int) -> Optional[Booking]:
        passenger = self.get_or_create_passenger(session, user_id, name, phone)

        flight = self.flight_repo.get_by_id(session, flight_id)
        if not flight:
            raise ValueError("Flight not found")
        if flight.status in (FlightStatus.cancelled, FlightStatus.landed):
            raise ValueError("Flight is not available for booking")

        seat = self.seat_repo.get_seat_by_id(session, seat_id)
        if not seat:
            raise ValueError("Seat not found")
        if seat.plane_id != flight.plane_id:
            raise ValueError("Seat does not belong to this flight's plane")

        exist = self.booking_repo.check_booking(session, seat_id, flight_id)
        if exist and exist.booking_status == BookingStatus.active:
            raise ValueError("Seat is already booked for this flight")

        pnr = self.generate_pnr()
        while self.booking_repo.get_by_pnr(session, pnr):
            pnr = self.generate_pnr()

        new_booking = Booking(
            pnr=pnr,
            passenger_id=passenger.id,
            flight_id=flight_id,
            seat_id=seat_id,
            price_paid=flight.price_per_seat,
            booking_status=BookingStatus.active)
        try:
            return self.booking_repo.create(session, new_booking)
        except Exception:
            raise ValueError("Failed to create booking")

    def cancel_booking(self, session: Session, booking_id: int, cancelled_by_airline: bool = False) -> Optional[Booking]:
        booking = self.booking_repo.get_by_id(session, booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.booking_status != BookingStatus.active:
            raise ValueError("Booking has been cancelled already")
        status = BookingStatus.cancelled_by_airline if cancelled_by_airline else BookingStatus.cancelled_by_passenger
        try:
            return self.booking_repo.cancel_booking(session, booking_id, status)
        except Exception:
            raise ValueError("Failed to cancel booking")

    def get_booking_by_id(self, session: Session, booking_id: int) -> Optional[Booking]:
        booking = self.booking_repo.get_by_id(session, booking_id)
        if not booking:
            raise ValueError("Booking not found")
        return booking

    def get_booking_by_pnr(self, session: Session, pnr: str) -> Optional[Booking]:
        booking = self.booking_repo.get_by_pnr(session, pnr)
        if not booking:
            raise ValueError("Booking not found")
        return booking

    def get_bookings_by_passenger(self, session: Session, passenger_id: int) -> List[Booking]:
        if not self.passenger_repo.get_by_id(session, passenger_id):
            raise ValueError("Passenger not found")
        return self.booking_repo.get_by_passenger_id(session, passenger_id)

    def get_bookings_by_flight(self, session: Session, flight_id: int) -> List[Booking]:
        if not self.flight_repo.get_by_id(session, flight_id):
            raise ValueError("Flight not found")
        return self.booking_repo.get_by_flight_id(session, flight_id)

    def get_active_bookings_per_flight(self, session: Session, flight_id: int) -> List[Booking]:
        if not self.flight_repo.get_by_id(session, flight_id):
            raise ValueError("Flight not found")
        return self.booking_repo.active_bookings_per_flight(session, flight_id)




