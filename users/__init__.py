from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from users import schemas

router = APIRouter(prefix="/user")

@router.post("/login", status_code=HTTPStatus.CREATED)
def login(user: schemas.UserBase):
    if "@" not in user.email:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid e-mail")
    return {"id": 1, "email": user.email, "password": user.password}