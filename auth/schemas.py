from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str


class UserCreate(User):
    confirm_password:str