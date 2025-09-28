from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Photo
from app.db.scheme.photo import PhotoCreate
from sqlalchemy import select, or_, desc, func
from typing import Optional

#사진은 로컬폴더나, 외부환경(외부스토리지)에 저장


class PhotoCrud:
    @staticmethod
    async def create(db:AsyncSession,
                     user_id:int, 
                     review_id:int, 
                     img_url:str):

        photo = Photo(user_id=user_id, review_id=review_id,img_url=img_url)
        db.add(photo)
        await db.flush()
        return photo
    
    @staticmethod
    async def get_all(db:AsyncSession, review_id:int):
        query = select(Photo).where(Photo.review_id==review_id).order_by(desc(Photo.created_at))
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def delete_by_id(db:AsyncSession, photo_id:int, user_id:int):
        photo = await db.get(Photo, photo_id)
        if photo and photo.user_id == user_id:
            #파일삭제
            await db.delete(photo)
            await db.flush()
            return True
        return False
    