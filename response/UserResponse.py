from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    nickname: str
    sex: str
    type_access: str
    
    class Config:
        from_attributes = True