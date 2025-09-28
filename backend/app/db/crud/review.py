from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Review
from app.db.scheme.review import ReviewCreate, ReviewUpdate
from sqlalchemy import select, or_, desc
from typing import Optional

class ReviewCrud:

    #Create    
    @staticmethod
    async def create(
        db:AsyncSession, 
        review_data:ReviewCreate,
        user_id: int,
        trip_id: int) -> Review:

        review_dict = review_data.model_dump()
        review_dict['user_id'] = user_id
        review_dict['trip_id'] = trip_id
        new_review = Review(**review_dict)
        db.add(new_review)
        await db.flush()
        return new_review
    
    #Read
    #review_id로 조회 / username,like_count,photos ->service query조회필요
    @staticmethod
    async def get_id(db:AsyncSession, review_id:int) -> Optional[Review]:
        return await db.get(Review, review_id)
    
    #reveiw-list 조회 trip에속한 리뷰만
    @staticmethod
    async def get_all(db:AsyncSession,
                      trip_id:int,
                      search:Optional[str]=None,
                      limit:int=10,
                      offset:int = 0
                      ):
        #데이터선택
        query = select(Review).where(Review.trip_id == trip_id)

        #검색 기능 조건
        if search:
            query = query.where(or_(Review.title.ilike(f'%{search.strip()}%'),
                                    Review.content.ilike(f'%{search.strip()}%')))
        #페이지네이션
        query = query.limit(limit).offset(offset)

        result = await db.execute(query)
        return result.scalars().all() #rows=result.scalars().all()
    
    #Update(review_id)
    @staticmethod
    async def update_by_id(db:AsyncSession, review_id:int, review:ReviewUpdate, user_id:int) -> Optional[Review]:
        db_review = await db.get(Review, review_id)
        if db_review:
            update_review = review.model_dump(exclude_unset=True) #review:ReviewUpdate
            for field, value in update_review.items():
                setattr(db_review, field, value)
            await db.flush()
            return db_review
        return None
    
    #Delete
    @staticmethod
    async def delete_by_id(db:AsyncSession, review_id:int) -> bool:
        review = await db.get(Review, review_id)
        if review:
            await db.delete(review)
            await db.flush()
            return True
        return False

class LikeCrud:
    pass
    
