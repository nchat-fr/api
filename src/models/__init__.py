from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.database import Base

import datetime


class Users(Base):
    __tablename__ = "users"
    extend_existing = True

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    mail = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class Messages(Base):
    __tablename__ = "messages"
    extend_existing = True

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    room = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("Users")
