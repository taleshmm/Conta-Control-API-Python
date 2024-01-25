from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from users import schemas, crud
from database import get_db
from sqlalchemy.orm import Session
from response import UserResponse, CreateUserResponse
from auth.utils import verify_token

router = APIRouter(prefix="/user", dependencies=[Depends(verify_token)])

@router.get("", response_model=list[UserResponse], status_code=HTTPStatus.OK )
def read_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    response = crud.get_users(db, skip, limit)
    return response

@router.post("", response_model=CreateUserResponse, status_code=HTTPStatus.CREATED)
def created_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    response = crud.create_user(db, user)
    return response

@router.get("/email", response_model=UserResponse, status_code=HTTPStatus.OK)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    response = crud.get_user_email(db, email)
    if response:
      user_dict = response.__dict__.copy()       
      user_dict['type_access'] = response.type_access.type_access  
      user_response = UserResponse(**user_dict)
      return user_response
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'User not found')