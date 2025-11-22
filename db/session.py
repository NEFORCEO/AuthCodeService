from typing import Annotated

from db.base import Model
from db.engine import engine, async_session

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
        
        
async def get_session():
    async with async_session() as session:
        yield session
        
SessionDep = Annotated[AsyncSession, Depends(get_session)]