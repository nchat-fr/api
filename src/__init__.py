from src.app import app
import src.models as models
from src.database import engine

print("inital database")
models.Base.metadata.create_all(bind=engine, checkfirst=True)
