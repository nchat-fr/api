from fastapi import APIRouter, Depends, Request, Response, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_
from pydantic import BaseModel, Field
from PIL import Image

import os.path
import src.models as models
import src.utils.exceptions as exceptions
from src.utils.webtokens import *
from src.database import get_db
from src.middlewares import auth_required

router = APIRouter()


@router.get("/{user_id}/image")
@auth_required()
def get_user_profile_picture(user_id: int, request: Request):
    if not os.path.isfile(f"storage/profiles_pictures/{user_id}.jpg"):
        return FileResponse(f"storage/profiles_pictures/default.jpg")
    return FileResponse(f"storage/profiles_pictures/{user_id}.jpg")


@router.post("/{user_id}/image")
@auth_required()
def set_user_profile_picture(user_id: int, request: Request, file: UploadFile):
    token = request.cookies.get("authenticator")
    identity = retrieve_access_token(token)
    if identity["id"] != user_id:
        raise exceptions.permissionDenied()

    image = Image.open(file.file).resize((128, 128))
    image.save(f"storage/profiles_pictures/{user_id}.jpg")
    image.close()
