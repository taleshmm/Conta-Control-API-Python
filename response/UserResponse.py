from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    nickname: str
    sex: str
    type_access: str
    
    class ConfigDict:
        from_attributes = True