from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_
from pydantic import BaseModel, Field

import src.models as models
import src.utils.exceptions as exceptions
from src.utils.webtokens import *
from src.database import get_db
from src.middlewares import auth_required

router = APIRouter()


class RegisterUserPayload(BaseModel):
    mail: str
    username: str = Field(..., min_length=3, max_length=25)
    password: str


class LoginUserPayload(BaseModel):
    mail: str
    password: str


@router.get("/")
@auth_required()
def logged_as(request: Request):
    token = request.cookies.get("authenticator")
    return retrieve_access_token(token)


@router.post("/login")
def login(body: LoginUserPayload, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.mail == body.mail).first()
    if user is None:
        raise exceptions.notFound()

    if not verify_password(body.password, user.password):
        raise exceptions.permissionDenied()

    token = create_access_token(user)
    response.set_cookie(
        key="authenticator",
        value=token,
        max_age=24 * 3600,
        secure=False,
        httponly=True
    )

    return retrieve_access_token(token)


@router.post("/register", status_code=201)
def register(body: RegisterUserPayload, db: Session = Depends(get_db)):
    user = (
        db.query(models.Users)
        .filter(
            or_(models.Users.username == body.username, models.Users.mail == body.mail)
        )
        .first()
    )
    if user is not None:
        raise exceptions.conflict()

    db.add(
        models.Users(
            mail=body.mail,
            username=body.username,
            password=hash_password(body.password),
        )
    )
    db.commit()


@router.delete("/", status_code=204)
@auth_required()
def logout(request: Request, response: Response):
    response.delete_cookie("authenticator")
