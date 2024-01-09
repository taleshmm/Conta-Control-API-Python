from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from users import schemas, crud
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user")

@router.post("/login", status_code=HTTPStatus.CREATED)
def login(user: schemas.UserBase):
    if "@" not in user.email:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid e-mail")
    return {"id": 1, "email": user.email, "password": user.password}

@router.get("", response_model=list[schemas.User] , status_code=HTTPStatus.OK)
def read_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users

@router.post("", status_code=HTTPStatus.CREATED)
def created_user(user: schemas.User, email: schemas.UserBase, hashed_password: schemas.UserCreate):
    pass