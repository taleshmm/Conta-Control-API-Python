from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from database import models


def get_permission(db: Session):
  try:
    permissions = db.query(models.Permission)
    return permissions
  except DatabaseError as db_error:
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Database Error - {db_error}")
  except Exception as error:
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Internal Server Error - {error}")
  
def create_permission(db: Session, type_permission: str):
    try:
      existing_permission = db.query(models.Permission).filter_by(type_access=type_permission).first()

      if existing_permission:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Permission already exists id: {existing_permission.id}, type: {existing_permission.type_access}")
      
      db_permission = models.Permission(type_access=type_permission)
      db.add(db_permission)
      db.commit()
      db.refresh(db_permission)
      return db_permission
    except Exception as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Internal Server Error - {error}")