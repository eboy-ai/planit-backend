from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    usename: str
    email:EmailStr
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[str] = None
    is_superuser: Optional[str] = None

# 내부 사용용
# 3. 출력 (API 응답)
class UserInDBBase(BaseModel):
    # DB 모델의 필드와 일치
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool