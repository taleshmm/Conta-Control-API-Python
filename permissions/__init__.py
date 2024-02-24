from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.utils import verify_token
from database import get_db
from permissions import crud, schemas

router = APIRouter(prefix="/permission", dependencies=[Depends(verify_token)])

@router.get("", response_model=list[schemas.Permission], status_code=HTTPStatus.OK)
def read_permission(db: Session = Depends(get_db)):
  permission = crud.get_permission(db)
  return permission

@router.post("", response_model=schemas.Permission, status_code=HTTPStatus.CREATED)
def created_permission(type_access: str, db: Session = Depends(get_db), ):
  permissions = crud.create_permission(db, type_access)
  return permissions