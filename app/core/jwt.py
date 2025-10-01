from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.settings import settings
from fastapi import HTTPException, status
from typing import Optional

#토큰 생성
def create_access_token(data:dict, expires_time: Optional[int] = 15):
  exp=datetime.utcnow() +timedelta(minutes=expires_time)
  data["exp"]=exp
  return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

#토큰 검증
def verify_access_token(token: str):
    try:
        return jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
