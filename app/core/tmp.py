from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.db.model.user import User
##### 임시 파일 , 토큰 의존성 주입 생성후 삭제예정 
async def get_user_id(db: AsyncSession = Depends(get_db)) -> int:
    # users 테이블에서 첫 번째 유저 가져오기
    result = await db.execute(select(User.id).limit(1))
    user_id = result.scalar_one_or_none()

    if not user_id:
        raise HTTPException(status_code=404, detail="No users found in DB")

    return user_id

### 삭제예정