from pydantic import BaseModel

class CreateUserResponse(BaseModel):
  id: int
  email: str
  name: str
  
  class ConfigDict:
    from_attributes = True
    
    from pydantic import BaseModel
