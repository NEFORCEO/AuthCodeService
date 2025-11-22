from db.base import Model

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from config import TABLE_PENDING, TABLE_USERS


class User(Model):
    __tablename__ = TABLE_USERS
    username: Mapped[str] = mapped_column(String, primary_key=True)
    code: Mapped[int] = mapped_column(Integer, index=True)
    
class PendingUser(Model):
    __tablename__ = TABLE_PENDING
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(String, default="user")
    