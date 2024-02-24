from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from accounts import crud, schemas
from auth.utils import verify_token
from database import get_db

router =  APIRouter(prefix="/account", dependencies=[Depends(verify_token)])

@router.get("", response_model=list[schemas.AccountModel], status_code=HTTPStatus.OK)
def read_all_accounts(id_user: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    response = crud.get_read_all_accounts(db, id_user, skip, limit)
    return response

@router.get("/id", response_model=schemas.AccountRequest, status_code=HTTPStatus.OK)
def read_by_unique_account(id_user: int, id_account, db: Session = Depends(get_db)):
    response = crud.get_read_unique_account(db, id_user, id_account)
    return response

@router.post("", response_model=schemas.CreateAccount, status_code=HTTPStatus.CREATED)
def create_account(account: schemas.CreateAccount, db: Session = Depends(get_db)):
    response = crud.create_account(db, account)
    return response

@router.put("", status_code=HTTPStatus.OK)
def update_account(id_user: int, account: schemas.UpdateAccount, db: Session = Depends(get_db)):
    response = crud.update_account(db, id_user, account)
    return response

@router.delete("", status_code=HTTPStatus.OK)
def delete_account(id_user: int, id_account: int, db: Session = Depends(get_db)):
    response = crud.delete_account(db, id_user, id_account)
    return response