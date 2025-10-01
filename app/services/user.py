from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from datetime import datetime
from app.db.crud import user as user_crud


async def register_user(db: AsyncSession, username: str, email: str, password: str):
    # 중복 이메일 체크
    existing_email = await user_crud.get_user_by_email(db, email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 중복 username 체크
    existing_username = await user_crud.get_user_by_username(db, username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    hashed_pw = hash_password(password)
    return await user_crud.create_user(db, username, email, hashed_pw)


async def login_user(db: AsyncSession, email: str, password: str) -> str | None:
    user = await user_crud.get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None

    await db.commit()
    await db.refresh(user)

    return create_access_token(data={"sub": str(user.id)})
