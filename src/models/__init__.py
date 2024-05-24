from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    mail = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
