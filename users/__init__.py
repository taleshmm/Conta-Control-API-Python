from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.utils import verify_token
from database import get_db
from response import CreateUserResponse, UserResponse
from users import crud, schemas

router = APIRouter(prefix="/user", dependencies=[Depends(verify_token)])

@router.get("", response_model=list[UserResponse], status_code=HTTPStatus.OK )
def read_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    response = crud.get_users(db, skip, limit)
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

@router.get("/id", response_model=UserResponse, status_code=HTTPStatus.OK)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    response = crud.get_user_by_id(db, id)
    if response:
        user_dict = response.__dict__.copy()
        user_dict['type_access'] = response.type_access.type_access
        user_response = UserResponse(**user_dict)
        return user_response
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'User not found')

@router.delete("", status_code=HTTPStatus.OK)
def delete_user(email: str = None, id: int = None, db: Session = Depends(get_db)):
    response = crud.delete_user_db(db, email, id)
    if response:
        return f"User {response} deleted with success."
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'User not found')

@router.put("", status_code=HTTPStatus.OK)
def update_user(user = schemas.UserBase, db: Session = Depends(get_db)):
    response = crud.updated_user(db, user)
    return response