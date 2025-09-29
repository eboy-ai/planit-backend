from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.settings import settings


async_engine = create_async_engine(settings.database_url, echo=False)


AsyncsessionLocal = sessionmaker(
    autocommit = False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base=declarative_base()

#비동기 세션 생성 함수
async def get_db():
    session = None
    try:
        session = AsyncsessionLocal()
        yield session
    except:
        pass
    finally:
        if session:
            await session.close()

#DB연결 경로 확인
print("DB URL:", settings.database_url)