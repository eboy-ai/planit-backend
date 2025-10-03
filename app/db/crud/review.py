from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Review, Like
from app.db.schema.review import ReviewCreate, ReviewUpdate
from sqlalchemy import select, or_, desc, func
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
    #review_id로 조회 / 
    #db.get- pk로만 조회가능 / db.execute (query)
    @staticmethod
    async def get_id(db:AsyncSession, review_id:int) -> Optional[Review]:
        #user 조회후 username 수정필요
        #리뷰객체 by_id
        db_review = await db.get(Review, review_id)
        if not db_review:
            return None
        
        #username     
        # user = await db.get(User, db_review.user_id)
        # if user: 
        #     db_review.username = user.username

        #like_count
        like_count= await LikeCrud.count_by_review(db,review_id)
        db_review.like_count=like_count

        return db_review
    
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
    @staticmethod
    async def exists(db:AsyncSession, user_id:int, review_id:int) -> bool:
        result = await db.execute(
            select(Like).where(Like.user_id == user_id,
                               Like.review_id == review_id))
        if result.scalar_one_or_none():
            return True
        else: 
            return False

    @staticmethod
    async def create(db:AsyncSession, user_id:int, review_id:int):
        like = Like(user_id=user_id,review_id=review_id)
        db.add(like)
        await db.flush()
        return like
    
    @staticmethod
    async def delete_id(db:AsyncSession, user_id:int, review_id:int):
        result = await db.execute(
            select(Like).where(Like.user_id == user_id,
                               Like.review_id == review_id))
        like = result.scalar_one_or_none()

        if like:
            await db.delete(like)
            await db.flush()
            return True
        return False

    #좋아요 개수 조회
    #(user_id,review_id)
    @staticmethod
    async def count_by_review(db:AsyncSession, review_id:int):
        result = await db.execute(select(func.count()).select_from(Like).where(Like.review_id == review_id))                                       
        return result.scalar_one() or 0

