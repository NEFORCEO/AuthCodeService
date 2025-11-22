from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import URL_DB

engine = create_async_engine(url=URL_DB)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

