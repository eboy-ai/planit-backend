from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.model import Review,Like
from app.db.schema.review import ReviewCreate, ReviewUpdate, LikeResponse, ReviewRead
from app.db.crud import ReviewCrud, LikeCrud
from sqlalchemy import select
from typing import Optional
from sqlalchemy import select, or_, desc, func


class ReviewService:
    #Create
    @staticmethod
    async def create(db:AsyncSession, 
                     review_data:ReviewCreate, 
                     user_id:int,
                     trip_id:int):
        try:
            db_review = await ReviewCrud.create(db, review_data,user_id,trip_id)

            await db.commit()
            await db.refresh(db_review)
            return db_review
        except Exception:
            raise
    
    #Read
    
    #trip id에 해당하는 list조회(R) - 여행별 리뷰
    @staticmethod
    async def get_all_review(db:AsyncSession,
                      trip_id:int,
                      search:Optional[str]=None,
                      limit:int=10,
                      offset:int = 0):
        db_review = await ReviewCrud.get_all(db,trip_id,search,limit,offset)

        return db_review

    #review_id
    @staticmethod
    async def get_review_username(db:AsyncSession,review_id:int):
        db_review = await ReviewCrud.get_id(db,review_id)  
        if not db_review:
            raise HTTPException(status_code=404, detail="리뷰가 없습니다")     
        return db_review
    #Update
    @staticmethod
    async def update_review_by_id(db:AsyncSession, review:ReviewUpdate, review_id:int, user_id:int):
               
        db_review = await ReviewCrud.get_id(db,review_id)
        if not db_review:
            raise HTTPException(status_code=404, detail='리뷰가없습니다')
        
        if db_review.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        update_data = await ReviewCrud.update_by_id(db, review_id, review,user_id)
        await db.commit()
        await db.refresh(update_data)
        return update_data
        

    #Delete
    @staticmethod
    async def delete_review_by_id(db:AsyncSession, review_id:int):
        db_review = await ReviewCrud.get_id(db,review_id)

        if not db_review:
            raise HTTPException(status_code=404, detail='리뷰없음')

        deleted_review = await ReviewCrud.delete_by_id(db,review_id)
        if deleted_review:            
            await db.commit()            
        return {'detail':'리뷰삭제됨'}


class LikeService:
    @staticmethod
    async def toggle(db:AsyncSession, user_id:Optional[int], review_id:int):
        if await LikeCrud.exists(db,user_id,review_id):
            await LikeCrud.delete_id(db,user_id,review_id)
            await db.commit()
            liked = False
        else:
            await LikeCrud.create(db,user_id,review_id)
            await db.commit()
            liked = True
        
        count = await LikeCrud.count_by_review(db,review_id)
        return LikeResponse(review_id=review_id,like_count=count,liked=liked)
                             #like_count = 좋아요 갯수, liked= 로그인한 유저 좋아요 토글
    #로그인 안해도 조회
    @staticmethod 
    async def count_likes(db:AsyncSession, review_id:int, user_id:int|None=None):        
        count = await LikeCrud.count_by_review(db,review_id)
        liked=False
        if user_id:
            liked = await LikeCrud.exists(db,user_id,review_id)
        return LikeResponse(review_id=review_id,like_count=count,liked=liked)
                             
