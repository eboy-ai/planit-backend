from fastapi import FastAPI
from contextlib import asynccontextmanager
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