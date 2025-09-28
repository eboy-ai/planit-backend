from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Review
from app.db.scheme.review import ReviewCreate, ReviewUpdate
from sqlalchemy import select
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
    
    #Delete
    @staticmethod
    async def delete_by_id(db:AsyncSession, review_id:int) -> bool:
        review = await db.get(Review, review_id)
        if review:
            await db.delete(review)
            await db.flush()
            return True
        return False
    
    #Update(review_id)
    @staticmethod
    async def update_by_id(db:AsyncSession, review_id:int, review:ReviewUpdate) -> Optional[Review]:
        db_review = await db.get(Review, review_id)
        if db_review:
            update_review = review.model_dump(exclude_unset=True) #review:ReviewUpdate
            for field, value in update_review.items():
                setattr(db_review, field, value)
            await db.flush()
            return db_review
        return None
    
