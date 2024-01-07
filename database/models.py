from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
  __tablename__ = 'user'
  
  id = Column(Integer, primary_key=True)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  nickname = Column(String)
  sex = Column(String)
  type_access_id = Column(Integer, ForeignKey('permission.id'))
  type_access = relationship("Permission", back_populates="owner")
  
class Permission(Base):
  __tablename__ = 'permission'
  
  id = Column(Integer, primary_key=True)
  type = Column(String, unique=True)
  owner = relationship("User", back_populates="type_access")

  
  