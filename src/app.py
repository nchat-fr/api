from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.sockets import sio_app
from src.routes import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.mount('/', app=sio_app)
