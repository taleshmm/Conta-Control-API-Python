from pydantic import BaseModel

from permissions import schemas


class UserBase(BaseModel):
    email: str  
    
class User(UserBase):
    id: int
    name: str
    nickname: str
    sex: str
    type_access: schemas.Permission
    
    class ConfigDict:
        from_attributes = True
        