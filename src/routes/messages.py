from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

import src.models as models
import src.utils.exceptions as exceptions
from src.utils.webtokens import *
from src.database import get_db
from src.middlewares import auth_required

router = APIRouter()


@router.get("/")
@auth_required()
def get_messages_history(request: Request, db: Session = Depends(get_db)):
    messages = db.query(models.Messages).filter(models.Messages.room == "/").order_by(models.Messages.created_at).all()

    for message in messages:
        message.user # lazy load user
    return messages
