from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from accounts import schemas
from database import models
from users.crud import get_user_by_id


def get_read_all_accounts(db: Session, id_user: int, skip: int = 0, limit: int = 20):
  try:
    accounts = db.query(models.ControlBills).filter(models.ControlBills.id_user == id_user).offset(skip).limit(limit).all()

    return accounts
  except Exception as error:
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Error:{error}') 

def get_read_unique_account(db: Session, id_user: int, id_account: int):
  try:
    get_account = db.query(models.ControlBills).filter(
            (models.ControlBills.id == id_account) & (models.ControlBills.id_user == id_user)
        ).first()
    
    if not get_account:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Account not found')


    return get_account
  except Exception as error:
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Error: {error}') 

def create_account(db: Session, account: schemas.CreateAccount):
    try:
        existing_user = get_user_by_id(db, account.id_user)
        
        if not existing_user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'User not found')
        
        db_account = models.ControlBills(id_user=account.id_user, type_account=account.type_account, name_account=account.name_account, value_total=account.value_total, installments=account.installments, value_installments=account.value_installments, date_buy=account.date_buy)
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Error: {error}')
    
def update_account(db: Session, id_user: int, account: schemas.UpdateAccount):
    try:
        existing_user = get_user_by_id(db, id_user)
            
        if not existing_user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'User not found')
        
        get_account = get_read_unique_account(db, id_user, account.id_account)
        
        if not get_account:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Account not found')
        
        get_account.type_account = account.type_account
        get_account.name_account = account.name_account
        get_account.value_total = account.value_total
        get_account.installments = account.installments
        get_account.value_installments = account.value_installments
        get_account.date_buy = account.date_buy
        
        db.commit()
        
        {'message': 'Account updated successfully', 'account': get_account}
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'Error:{error}')
        
def delete_account(db: Session, id_user: int, id_account: int):
    try:
        get_account = get_read_unique_account(db, id_user, id_account)
   
        if not get_account:
          raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Account not found')
        
        db.delete(get_account)  
        db.commit()
        
        response = {"name": get_account.name_account, "message": "Delete account with success"}
        return response
     
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'{error}')
  
      
    
        
        
        
        
        