import datetime
import logging

from fastapi import FastAPI, Req, Request, Response

from client.lifespan import start_app
from api.router.router import router
from api.router.db_router import db_root


app = FastAPI(lifespan=start_app)


@app.middleware('http')
async def log_routers(request: Request, call_next) -> Response:
    start_time = datetime.now()
    
    logging.info(f"request: {request.method}, url: {request.url}")
    response = await call_next(request)
    
    duration = (datetime.now() - start_time).total_seconds()
    logging.info(f"answer: {response.status_code} | time: {duration:.2f}s")
    
    return response

app.include_router(router)
app.include_router(db_root)
