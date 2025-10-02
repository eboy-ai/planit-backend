from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.schema.user import UserCreate, UserResponse, UserLogin, UserUpdate, Token
from app.services.user import register_user,login_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login", response_model=Token)
async def login_for_user(user:UserLogin, db:AsyncSession=Depends(get_db)):
    access_token = await login_user(db, user.email, user.password)

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {"access_token":access_token, "token_type":"bearer"}

@router.post("/join", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await register_user(db, user.username, user.email, user.password)
    return new_user


