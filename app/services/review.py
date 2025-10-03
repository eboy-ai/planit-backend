from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.model import Review,Like,Trip
from app.db.schema.review import ReviewCreate, ReviewUpdate, LikeResponse, ReviewRead
from app.db.crud import ReviewCrud, LikeCrud
from sqlalchemy import select
from typing import Optional
from sqlalchemy import select, or_, desc, func

# by_relationship- responsebody에 유저이름, 좋아요 수 추가함수  
# #username  
def add_username(review:Review):    
    if review.users:
        review.username = review.users.username
    else:
        raise HTTPException(status_code=404,detail='작성자 정보 없음')
    return review
#like_count 
async def add_likecounts(db:AsyncSession,review:Review):           
    review.like_count=await LikeCrud.count_by_review(db,review.id)
    return review

class ReviewService:
    #Create
    @staticmethod
    async def create(db:AsyncSession,review_data:ReviewCreate, user_id:int,trip_id:int):
        #trip_id 유효성 검증
        trip = await db.get(Trip, trip_id)  #PK조회 전용
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='존재하지않는 여행계획입니다')
        
        db_review = await ReviewCrud.create(db, review_data,user_id,trip_id)
        # await db.commit() -get_db에서 commit 관리중 삭제     
        await db.refresh(db_review)
        
        #orm 반환용 / user주입 / like_count 초기값
        db_review = add_username(db_review)
        db_review.like_counts = 0
        return db_review
        
    
    #Read    
    #trip id에 해당하는 list조회(R) - 여행별 리뷰 / trip_id없을시 빈배열반환 []
    @staticmethod
    async def get_all_review(db:AsyncSession,
                      trip_id:int,
                      search:Optional[str]=None,
                      limit:int=10,
                      offset:int = 0):
        db_review = await ReviewCrud.get_all(db,trip_id,search,limit,offset)
        #orm 반환용 / user주입 / like_count 초기값
        if not db_review:
            return []
        for review in db_review:
            add_username(review)
            await add_likecounts(db,review)            
        return db_review

    #review_id로 개별조회
    @staticmethod
    async def get_review(db:AsyncSession,review_id:int):
        db_review = await ReviewCrud.get_id(db,review_id)  
        if not db_review:
            raise HTTPException(status_code=404, detail="리뷰가 없습니다")     
        if not db_review.users:
            raise HTTPException(status_code=404, detail='작성자 정보 없음')
        
        #username
        add_username(db_review)
        #like_count       
        await add_likecounts(db,db_review)

        return db_review
    
    #Update
    @staticmethod
    async def update_review_by_id(db:AsyncSession, review:ReviewUpdate, review_id:int, user_id:int):
               
        db_review = await ReviewCrud.get_id(db,review_id)
        if not db_review:
            raise HTTPException(status_code=404, detail='리뷰가없습니다')
        
        if db_review.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='로그인한 사용자만 수정가능')
        
        update_data = await ReviewCrud.update_by_id(db, review_id, review,user_id)
        await db.commit()
        await db.refresh(update_data)

        #username
        add_username(update_data)
        #like_count       
        await add_likecounts(db,update_data)

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
                             
