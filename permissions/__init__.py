from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from permissions import schemas, crud
from database import get_db
from sqlalchemy.orm import Session
from auth import utils

router = APIRouter(prefix="/permission")

@router.get("", response_model=list[schemas.Permission], status_code=HTTPStatus.OK)
def read_permission(db: Session = Depends(get_db)):
  permission = crud.get_permission(db)
  return permission

@router.post("", response_model=schemas.Permission, status_code=HTTPStatus.CREATED)
def created_permission(type_access: str, db: Session = Depends(get_db), ):
  permissions = crud.create_permission(db, type_access)
  return permissions