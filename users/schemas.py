from pydantic import BaseModel
from permissions import schemas

class UserBase(BaseModel):
    email: str  
    
class UserSecurity(BaseModel):
    password: str
    
class User(UserBase):
    id: int
    name: str
    nickname: str
    sex: str
    type_access: schemas.Permission
    
    class Config:
        from_attributes = True
        
        
class UserCreate(UserSecurity, UserBase):
    name: str
    nickname: str
    sex: str
    type_access: int
    class Config:
        from_attributes = True