from fastapi import FastAPI

from client.lifespan import start_app
from api.router.router import router
from api.router.db_router import db_root


app = FastAPI(lifespan=start_app)

app.include_router(router)
app.include_router(db_root)
