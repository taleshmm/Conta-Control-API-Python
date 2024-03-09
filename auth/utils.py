import time
from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.hash import pbkdf2_sha256

from auth import schemas
from auth.crud import get_user_email
from database import get_db

security = HTTPBearer()
SECRET_KEY = "secret"
ALGORITHM = "HS256"

def validate_user(db, email: str, password: str):
  user = get_user_email(db, email)
  if not user:
    return
  if not pbkdf2_sha256.verify(password, user.hashed_password): 
    return
  
  return user
  
def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
  user = validate_user(db, credentials.username, credentials.password)
  if not user:
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=f'User or password incorrect', headers={'WWW-Authenticate': 'Bearer'})
  return user

def create_token(credentials: schemas.UserAuthentication, db=Depends(get_db)):
  user = validate_user(db, credentials.email, credentials.password)
  if not user:
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=f'User or password incorrect', headers={'WWW-Authenticate': 'Bearer'})
  
  expiration_time = datetime.utcnow() + timedelta(minutes=60)
  token = jwt.encode({"email": credentials.email, "exp": expiration_time}, SECRET_KEY, ALGORITHM)
  unix_time = time.mktime(expiration_time.timetuple())
  return {
          "token": token,
          "exp": unix_time
          }

def verify_token(token: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)):
  try:
    data = jwt.decode(token.credentials, SECRET_KEY, algorithms=ALGORITHM)
  except jwt.exceptions.DecodeError:
    raise HTTPException(HTTPStatus.BAD_REQUEST, detail="Invalid Token")
  except jwt.exceptions.ExpiredSignatureError:
    raise HTTPException(HTTPStatus.BAD_REQUEST, "Token expired")
  
  email = data.get("email")
  user = get_user_email(db, email)
  if not user:
    raise HTTPException(HTTPStatus.UNAUTHORIZED, "Credentials invalids")
  
  return data