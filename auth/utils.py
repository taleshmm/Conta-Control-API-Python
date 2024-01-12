from database import get_db
from users.crud import get_user_email
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException
from http import HTTPStatus


security = HTTPBasic()

def validate_user(db, email: str, password: str):
  user = get_user_email(db, email)
  if not user:
    return
  if not user.hashed_password == f'{password}+notreallyhashed': 
    return
  
  return user
  
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security), db = Depends(get_db)):
  user = validate_user(db, credentials.username, credentials.password)
  if not user:
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=f'User or password incorrect', headers={'WWW-Authenticate': 'Basic'})
  return user
