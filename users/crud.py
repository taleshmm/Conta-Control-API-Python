from sqlalchemy.orm import Session
from database import models
from users import schemas
from fastapi import HTTPException
from http import HTTPStatus
from response.UserResponse import UserResponse

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
    existing_user = db.query(models.User).filter_by(email=user.email).first()
    
    if existing_user:
      raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"User already exists: \n id: {existing_user.id} \n email: {existing_user.email} \n name: {existing_user.name}")
    
    faked_hashed = f'{user.password}+notreallyhashed'
    db_user = models.User(email=user.email, name=user.name, hashed_password=faked_hashed, nickname=user.nickname, sex=user.sex, type_access_id=user.type_access)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    result = {'id': db_user.id, 'name': db_user.name, 'e-mail': db_user.email}
    return result
    
  except Exception as error:
    db.rollback()
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Internal Server Error - {error}')