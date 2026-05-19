from typing import Optional, List
from sqlalchemy.orm import Session
from models.plane import Plane
from sqlalchemy import select


class PlaneRepo:
    def create(self, session: Session, plane: Plane) -> Optional[Plane]:
        try:
            session.add(plane)
            session.flush()
            return plane
        except Exception as e:
            session.rollback()
            raise e

    def get_by_id(self, session: Session, plane_id: int) -> Optional[Plane]:
        try:
            stmt = select(Plane).where(Plane.id == plane_id)
            return session.scalar(stmt)
        except Exception as e:
            raise e

    def get_all(self, session: Session) -> List[Plane]:
        try:
            stmt = select(Plane)
            return session.scalars(stmt).all()
        except Exception as e:
            raise e

    def delete(self, session: Session, plane_id: int) -> Optional[Plane]:
        try:
            stmt = select(Plane).where(Plane.id == plane_id)
            plane = session.scalar(stmt)
            if plane:
                session.delete(plane)
                session.flush()
            return plane
        except Exception as e:
            session.rollback()
            raise e




