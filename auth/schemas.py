from pydantic import BaseModel

class UserAuthentication(BaseModel):
    email: str
    password: str

class UserCreate(UserAuthentication):
    confirm_password:str