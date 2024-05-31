from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base


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
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("Users")
