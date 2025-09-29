from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import trip_router, city_router
# from fastapi.concurrency import asynccontextmanager

from app.db.database import async_engine, Base
import test


from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# 로드시 테이블 자동생성
@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(trip_router.router)
app.include_router(city_router.router)