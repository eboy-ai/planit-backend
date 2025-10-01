from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import settings

DATABASE_URL = (
    f"mysql+aiomysql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True )

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Base.metadata.create_all(bind=engine)
# 이 명령어는 동기 시스템에서 사용가능한 테이블 생성 명령어

async def inin():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)