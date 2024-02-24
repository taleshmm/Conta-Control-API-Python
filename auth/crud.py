from http import HTTPStatus

from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session

from auth import schemas
from database import models


def get_user_email(db: Session, email: str):
  try:
    db_user = db.query(models.User).filter_by(email=email).first()
    return db_user
  except Exception as error:
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Internal Server Error - {error}')
  
def create_user(db: Session, user: schemas.UserCreateAuth):
  try:
    existing_user = get_user_email(db, user.email)

    if existing_user:
      raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"User already exists email: {existing_user.email}")
    
    hashed_password = pbkdf2_sha256.hash(user.password)
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password, nickname=user.nickname, sex=user.sex, type_access_id=user.type_access)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
  except Exception as error:
      db.rollback()
      raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Internal Server Error - {error}')
  


