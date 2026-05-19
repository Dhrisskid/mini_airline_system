from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User


class UserRepo:
    def create(self, session: Session, user: User) -> Optional[User]:
        try:
            session.add(user)
            session.flush()
            return user
        except Exception as e:
            session.rollback()
            raise e

    def get_by_id(self, session: Session, user_id: int) -> Optional[User]:
        try:
            us = select(User).where(User.id == user_id)
            return session.scalar(us)
        except Exception as e:
            raise e

    def get_by_email(self, session: Session, email: str) -> Optional[User]:
        try:
            us = select(User).where(User.email == email)
            return session.scalar(us)
        except Exception as e:
            raise e

    def update_password(self, session: Session, user_id: int, already_hashed_password: str) -> Optional[User]:
        try:
            us = select(User).where(User.id == user_id)
            user = session.scalar(us)
            if user:
                user.hashed_password = already_hashed_password
                session.flush()
            return user
        except Exception as e:
            session.rollback()
            raise e

    def update_status(self, session: Session, user_id: int, is_active: bool) -> Optional[User]:
        try:
            us = select(User).where(User.id == user_id)
            user = session.scalar(us)
            if user:
                user.is_active = is_active
                session.flush()
            return user
        except Exception as e:
            session.rollback()
            raise e

    def delete(self, session: Session, user_id: int) -> Optional[User]:
        try:
            us = select(User).where(User.id == user_id)
            user = session.scalar(us)
            if user:
                session.delete(user)
                session.flush()
            return user
        except Exception as e:
            session.rollback()
            raise e

        