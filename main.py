from fastapi import FastAPI
from persistence.dB import Base, engine
from routers import user_router, passenger_router, plane_router, seat_router, flight_router, booking_router
from models import user, passenger, plane, seat, flight, booking
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Airline API")

app.include_router(user_router.router)
app.include_router(passenger_router.router)
app.include_router(plane_router.router)
app.include_router(seat_router.router)
app.include_router(flight_router.router)
app.include_router(booking_router.router)

