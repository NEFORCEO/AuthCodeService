from fastapi import APIRouter
from sqlalchemy import select

from db.models import User, PendingUser
from db.session import SessionDep

db_root = APIRouter(prefix="/db", tags=["База данных"])

@db_root.get("/users")
async def get_users_db(db: SessionDep):
    users = await db.execute(select(User))
    return users.scalars().all()

@db_root.get("/pendings")
async def get_pending_db(db: SessionDep):
    users = await db.execute(select(PendingUser))
    return users.scalars().all()

