from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import  schemas
from database import get_db

router = APIRouter(prefix="/auth")

@router.post("/signup")
def signup(credentials: schemas.UserCreate, db:Session = Depends(get_db)):
    ...

  
   
    
     