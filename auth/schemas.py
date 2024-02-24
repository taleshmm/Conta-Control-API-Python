from pydantic import BaseModel


class UserAuthentication(BaseModel):
    email: str
    password: str

class UserCreate(UserAuthentication):
    confirm_password:str     
        
class UserCreateAuth(UserCreate):
    name: str
    nickname: str
    sex: str
    type_access: int
    class ConfigDict:
        from_attributes = True