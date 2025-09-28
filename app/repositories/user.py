# app/repositories/user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash # 보안 유틸리티 임포트
from typing import Optional, List, Any


# 1. Email로 사용자 조회
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()

# 2. Username으로 사용자 조회 (인증용)
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()

# 3. 사용자 생성 (CREATE)
async def create_user(db: AsyncSession, user: UserCreate) -> User:
    # 💡 여기서 비밀번호를 해싱합니다.
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        is_active=True, # 기본값
        is_superuser=False # 기본값
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# 4. ID로 사용자 조회 (READ)
async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    return await db.get(User, user_id)

# 5. 사용자 목록 조회 (READ)
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# 6. 사용자 업데이트 (UPDATE)
async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = await db.get(User, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True) # Pydantic v2
    
    # 비밀번호가 포함된 경우 해싱
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# 7. 사용자 삭제 (DELETE)
async def delete_user(db: AsyncSession, user_id: int) -> Optional[User]:
    db_user = await db.get(User, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return db_user
    return None