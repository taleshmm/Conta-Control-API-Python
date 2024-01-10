from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from users import schemas, crud
from database import get_db
from sqlalchemy.orm import Session
from response.UserResponse import UserResponse

router = APIRouter(prefix="/user")

@router.post("/login", status_code=HTTPStatus.CREATED)
def login(user: schemas.UserBase):
    if "@" not in user.email:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid e-mail")
    return {"id": 1, "email": user.email, "password": user.password}

@router.get("", response_model=list[UserResponse], status_code=HTTPStatus.OK)
def read_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    response = crud.get_users(db, skip, limit)
    return response

@router.post("", status_code=HTTPStatus.CREATED)
def created_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    response = crud.create_user(db, user)
    return response