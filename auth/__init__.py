from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import  utils, schemas, crud
from database import get_db

router = APIRouter(prefix="/auth")

@router.post("/signup")
def signup(credentials: schemas.UserAuthentication, db = Depends(get_db)):
   user = crud.create_user(db, credentials)
   token = utils.create_token(credentials, db)
   return {
        "user": user,
        "token": token
           }

@router.post("/login")
def login(token=Depends(utils.create_token)):
    return token

  
   
    
     