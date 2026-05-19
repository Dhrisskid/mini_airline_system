from typing import Optional
from models.user import User, UserRole
from models.passenger import Passenger
from repositories.user_repo import UserRepo
from repositories.passenger_repo import PassengerRepo
from schemas.requests.user_request import UserRequestModel, LoginRequestModel, AdminCreateUserModel
from sqlalchemy.orm import Session
from hashing.pass_hashing import hash_password, verify_password


class UserService:
    def __init__(self):
        self.user_repo = UserRepo()
        self.passenger_repo = PassengerRepo()

    def register(self, session: Session, user: UserRequestModel) -> Optional[User]:
        if self.user_repo.get_by_email(session, user.email):
            raise ValueError("Email already registered")
        hashed_pass = hash_password(user.password)
        new_user = User(email=user.email, hashed_password=hashed_pass, role=UserRole.passenger)
        try:
            return self.user_repo.create(session, new_user)
        except Exception:
            raise ValueError("Failed to register user")

    def create_admin(self, session: Session, user: AdminCreateUserModel) -> Optional[User]:
        if self.user_repo.get_by_email(session, user.email):
            raise ValueError("Email already registered")
        hashed_pass = hash_password(user.password)
        new_user = User(email=user.email, hashed_password=hashed_pass, role=user.role)
        try:
            return self.user_repo.create(session, new_user)
        except Exception:
            raise ValueError("Failed to create user")

    def log_in(self, session: Session, user: LoginRequestModel) -> Optional[User]:
        existing_user = self.user_repo.get_by_email(session, user.email)
        if not existing_user:
            raise ValueError("Invalid credentials")
        if not verify_password(user.password, existing_user.hashed_password):
            raise ValueError("Invalid credentials")
        if not existing_user.is_active:
            raise ValueError("Account is deactivated")
        return existing_user

    def get_user_by_id(self, session: Session, user_id: int) -> Optional[User]:
        user = self.user_repo.get_by_id(session, user_id)
        if not user:
            raise ValueError("User not found")
        return user

    def get_user_by_email(self, session: Session, email: str) -> Optional[User]:
        user = self.user_repo.get_by_email(session, email)
        if not user:
            raise ValueError("User not found")
        return user

    def update_password(self, session: Session, user_id: int, new_password: str) -> Optional[User]:
        if not self.user_repo.get_by_id(session, user_id):
            raise ValueError("User not found")
        try:
            hashed = hash_password(new_password)
            return self.user_repo.update_password(session, user_id, hashed)
        except Exception:
            raise ValueError("Failed to update password")

    def update_active_status(self, session: Session, user_id: int, is_active: bool) -> Optional[User]:
        if not self.user_repo.get_by_id(session, user_id):
            raise ValueError("User not found")
        try:
            return self.user_repo.update_status(session, user_id, is_active)
        except Exception:
            raise ValueError("Failed to update status")

    def delete_user(self, session: Session, user_id: int) -> Optional[User]:
        if not self.user_repo.get_by_id(session, user_id):
            raise ValueError("User not found")
        try:
            return self.user_repo.delete(session, user_id)
        except Exception:
            raise ValueError("Failed to delete user")




