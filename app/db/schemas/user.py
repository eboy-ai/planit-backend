from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.db.schemas import GroupResponse


# ----------------------
# 사용자 관련 스키마
# ----------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int


    # 🔑 그룹 정보 포함
    groups: List[GroupResponse] = []

    class Config:
        orm_mode = True
