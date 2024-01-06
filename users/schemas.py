from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str
    
class User(UserBase):
    name: str
    id: str
    nickname: str
    sex: str
    type_acess: str
    sales: float