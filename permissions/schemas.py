from pydantic import BaseModel

class Permission(BaseModel):
    id: int
    type_access: str
    
    class Config:
        from_attributes = True