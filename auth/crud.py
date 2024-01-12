from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session

from auth import schemas
from database import models


def get_user_by_email(db: Session, email:str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    return db_user

