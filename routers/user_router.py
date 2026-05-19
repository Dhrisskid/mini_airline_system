from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from persistence.dB import get_db
from services.user_service import UserService
from schemas.requests.user_request import UserRequestModel, LoginRequestModel, AdminCreateUserModel, UpdatePasswordRequest, UpdateActiveStatusRequest
from schemas.responses.user_response import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserRequestModel, db: Session = Depends(get_db)):
    try:
        return user_service.register(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/admin", response_model=UserResponse, status_code=201)
def create_admin(user: AdminCreateUserModel, db: Session = Depends(get_db)):
    try:
        return user_service.create_admin(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=UserResponse)
def login(user: LoginRequestModel, db: Session = Depends(get_db)):
    try:
        return user_service.log_in(db, user)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    try:
        return user_service.get_user_by_email(db, email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_service.get_user_by_id(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{user_id}/password", response_model=UserResponse)
def update_password(user_id: int, body: UpdatePasswordRequest, db: Session = Depends(get_db)):
    try:
        return user_service.update_password(db, user_id, body.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{user_id}/status", response_model=UserResponse)
def update_status(user_id: int, body: UpdateActiveStatusRequest, db: Session = Depends(get_db)):
    try:
        return user_service.update_active_status(db, user_id, body.is_active)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_service.delete_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))