from pydantic import BaseModel
from typing import Union
from permissions import schemas

class UserBase(BaseModel):
    email: str  
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    name: str
    id: str
    nickname: str
    sex: str
    type_access: schemas.Permission
    
    class Config:
        from_attributes = True