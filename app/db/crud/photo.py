from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Photo
from app.db.schema.photo import PhotoCreate
from sqlalchemy import select, or_, desc, func
from typing import Optional


#사진은 로컬폴더나, 외부환경(외부스토리지)에 저장


class PhotoCrud:
    @staticmethod
    async def create(db:AsyncSession,                      
                     review_id:int, 
                     filename:str,
                     data:bytes):    
        db_photo = Photo(review_id=review_id,filename=filename,data=data)
        db.add(db_photo)
        await db.flush()
        return db_photo
    
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
    