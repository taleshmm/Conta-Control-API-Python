from pydantic import BaseModel

class Permission(BaseModel):
    id: int
    type_access: str
    
    class ConfigDict:
        from_attributes = True