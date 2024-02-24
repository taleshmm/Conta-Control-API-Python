from datetime import date

from pydantic import BaseModel


class AccountModel(BaseModel):
    id: int
    id_user: int
    type_account: str
    name_account: str
    value_total: float
    installments: int
    value_installments:  float
    date_buy: date
    
class AccountRequest(BaseModel):
    type_account: str
    name_account: str
    value_total: float
    installments: int
    value_installments:  float
    date_buy: date
    
class CreateAccount(BaseModel):
    id_user: int
    type_account: str
    name_account: str
    value_total: float
    installments: int
    value_installments:  float
    date_buy: date
    
class UpdateAccount(BaseModel):
    id: int
    type_account: str
    name_account: str
    value_total: float
    installments: int
    value_installments:  float
    date_buy: date