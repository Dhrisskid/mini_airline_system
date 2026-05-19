from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from persistence.dB import get_db
from services.plane_service import PlaneService
from schemas.requests.plane_request import CreatePlaneRequest
from schemas.responses.plane_response import PlaneResponse

router = APIRouter(prefix="/planes", tags=["Planes"])
plane_service = PlaneService()


@router.post("/", response_model=PlaneResponse, status_code=201)
def create_plane(body: CreatePlaneRequest, db: Session = Depends(get_db)):
    try:
        return plane_service.create_plane(db, body.model, body.total_seats)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[PlaneResponse])
def get_all_planes(db: Session = Depends(get_db)):
    return plane_service.get_all_planes(db)


@router.get("/{plane_id}", response_model=PlaneResponse)
def get_plane(plane_id: int, db: Session = Depends(get_db)):
    try:
        return plane_service.get_plane_by_id(db, plane_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{plane_id}", response_model=PlaneResponse)
def delete_plane(plane_id: int, db: Session = Depends(get_db)):
    try:
        return plane_service.delete_plane(db, plane_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))