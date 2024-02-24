from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import models
from response import UserResponse
from users import schemas


def get_user_by_id(db: Session, id: int):
  try:
    db_user = db.query(models.User).filter_by(id=id).first()
    return db_user
  except Exception as error:
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Internal Server Error - {error}')
    print('An exception occurred')

def get_user_email(db: Session, email: str):
  try:
    db_user = db.query(models.User).filter_by(email=email).first()
    return db_user
  except Exception as error:
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Internal Server Error - {error}')
  
def get_users(db: Session, skip: int = 0, limit: int = 10):
  try:
    users = db.query(models.User).offset(skip).limit(limit).all()
    
    user_responses = [
      UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        nickname=user.nickname,
        sex=user.sex,
        type_access=user.type_access.type_access  
            )
            for user in users
        ]

    return user_responses
  except Exception as error:
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Internal server error = {error}') 

def create_user(db: Session, user: schemas.UserCreate):
  try:
    existing_user = get_user_email(db, user.email)

    if existing_user:
      raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"User already exists email: {existing_user.email}")
    
    faked_hashed = f'{user.password}+notreallyhashed'
    db_user = models.User(email=user.email, name=user.name, hashed_password=faked_hashed, nickname=user.nickname, sex=user.sex, type_access_id=user.type_access)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
  except Exception as error:
    db.rollback()
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Internal Server Error - {error}')
  
def delete_user_db(db: Session, user_email: str = None, user_id: int = None):
  try:
    query = db.query(models.User)
    if user_email is not None:
      query = query.filter_by(email=user_email)
    if user_id is not None:
      query = query.filter_by(id=user_id)
    user = query.first()
    if user:
      db.delete(user)
      db.commit()
      return user.email
    return 
  except Exception as error:
    db.rollback()
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Internal Server Error = {error}')
    
  
  