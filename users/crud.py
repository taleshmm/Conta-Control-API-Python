from sqlalchemy.orm import Session
from database import models
from users import schemas

def get_users(db: Session, skip: int = 0, limit: int = 10):
  users = db.query(models.User).offset(skip).limit(limit)
  return users