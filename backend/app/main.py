import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api import auth_router, items_router, lists_router
from app.db.database import close_engine, test_connection

load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI(title="ada-to-do-app")
app.include_router(auth_router)
app.include_router(lists_router)
app.include_router(items_router)


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    await test_connection()


@app.on_event("shutdown")
async def on_shutdown():
    await close_engine()
