from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
  __tablename__ = 'user'
  
  id = Column(Integer, primary_key=True)
  email = Column(String, unique=True, index=True)
  name = Column(String)
  hashed_password = Column(String)
  nickname = Column(String)
  sex = Column(String)
  type_access_id = Column(Integer, ForeignKey('permission.id'))
  type_access = relationship("Permission", back_populates="owner")
  control_bills = relationship("ControlBills", back_populates="user")
  
class Permission(Base):
  __tablename__ = 'permission'
  
  id = Column(Integer, primary_key=True)
  type_access = Column(String, unique=True)
  owner = relationship("User", back_populates="type_access")

class ControlBills(Base):
    __tablename__ = 'controlBills'
   
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    type_account = Column(String)
    name_account = Column(String)
    value_total = Column(Numeric)
    installments = Column(Integer)
    value_installments =  Column(Numeric)
    date_buy = Column(Date)
    
    user = relationship("User", back_populates="control_bills")
   
   
  