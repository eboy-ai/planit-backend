from fastapi import APIRouter, Depends, Request, Query
from app.db.database import get_db
from app.db.model import Like
from app.db.schema.review import LikeResponse, LikeCreate
from app.services import LikeService
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import InvalidTokenError, ExpiredSignatureError
from app.core.tmp import get_user_id
router = APIRouter(prefix='/reviews',tags=['Like'])

#액세스 토큰이 없어도 예외던지지 않겠다. 그냥 None반환
# 로그인 안해도 볼수있는페이지에서 사용할때
async def get_user_id_option(request:Request):
    access_token=request.cookies.get("access_token")
    if not access_token:
        return None
    return 1
################################### 더미데이터

#로그인한 유저 좋아요 토글 요청 + 좋아요 갯수
@router.post('/{review_id}/likes', response_model=LikeResponse)
async def toggle_like(review_id:int,
                user_id:int=Depends(get_user_id),
                db:AsyncSession=Depends(get_db)):
    return await LikeService.toggle(db,user_id,review_id)
#페이지 로드시 좋아요 수 노출
@router.get('/{review_id}/likes', response_model=LikeResponse)
async def get_likes(review_id:int,
                    user_id:int|None = Depends(get_user_id_option),
                    db:AsyncSession=Depends(get_db)):
    return await LikeService.count_likes(db,review_id,user_id)
