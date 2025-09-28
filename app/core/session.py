from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Generator
from app.core.settings import settings

#비동기 에진 생성
# settings.py의 async_db_url 속성을 사용하여 MySql 비동기 연결 URL을 가져온다
engin = create_async_engine(
    settings.async_db_url,
    echo=True,
    pool_pre_poing=True
)

# 비동기 세션 로컬 클래스 생성
AsyncSessionLocal = sessionmaker(
    autocommit = False,
    autoflush= False,
    bind=engin,
    class_=AsyncSession,
    expire_on_commit=False
)

#DI 설정
async def get_db() -> Generator[AsyncSession,None, None]:
    async with AsyncSessionLocal() as session:
        yield session