import random
from sqlalchemy import select
from db.models import User
from db.session import SessionDep

async def generate_code(db: SessionDep):
    while True:
        code = random.randint(1000000, 9999999)
        existing = await db.execute(select(User).where(User.code == code))
        if not existing.scalar_one_or_none():
            return code


