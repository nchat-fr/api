from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.sockets import sio_app
from src.routes import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://194.164.48.49", "http://85.215.133.119"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["User"])
app.include_router(message_router, prefix="/messages", tags=["Messages"])
app.mount("/", app=sio_app)
