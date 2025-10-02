from fastapi import FastAPI
from app.routers import user
from app.db.database import inin, engine


app=FastAPI()


@app.on_event('startup')
async def startup_init():
    import app.db.model.group
    import app.db.model.user
    await inin()
    print("Database engine connect")
#SQLAlchemy의 비동기 MySQL 드라이버(aiomysql)와 서버 종료 타이밍 사이의 충돌
#해결책: engine.dispose() 누락
@app.on_event('shutdown')
async def shutdown_event():
    await engine.dispose()
    print("Database engine disposed successfully")


app.include_router(
    user.router,
    prefix="/users",
    tags=["users"]
)

