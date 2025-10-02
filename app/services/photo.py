from fastapi import HTTPException,status, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.model import Photo, Review
from app.db.schema.photo import PhotoCreate
from app.db.crud import PhotoCrud
from sqlalchemy import select
from typing import Optional

class PhotoService:
    @staticmethod
    async def create_image(db:AsyncSession,review_id:int,file:UploadFile):
        contents = await file.read()  #업로드된 파일을 읽어옴
        db_photo = await PhotoCrud.create(db=db,
                                          review_id=review_id,                                    
                                          filename=file.filename,
                                          content_type=file.content_type,
                                          data=contents)
        await db.commit()
        await db.refresh(db_photo)        
        return db_photo
    
    #사진 리스트 조회
    @staticmethod
    async def get_all_photo(db:AsyncSession,review_id:int):
        db_photo = await PhotoCrud.get_all(db,review_id)
        # if not db_photo:
        #     raise
        print(db_photo)
        return db_photo
        
        #파일 확장자 mime-type
    
    #사진 한개(대표이미지/원본조회) 조회
    @staticmethod
    async def get_photo(db:AsyncSession,review_id:int,photo_id:int):        
        query = select(Photo).where(Review.id == review_id,
                                    Photo.id == photo_id)
        #예외처리
        result = await db.execute(query)
        db_photo = result.scalar_one_or_none()
        return db_photo
    
    #사진 삭제
    @staticmethod
    async def delete_photo_by_id(db:AsyncSession,photo_id:int,user_id:int)->bool:
        db_photo = await PhotoCrud.get_photo_id(db,photo_id)
        if not db_photo:
            raise HTTPException(status_code=404, detail='사진없음')
        
        deleted_photo = await PhotoCrud.delete_by_id(db,photo_id,user_id)
        if deleted_photo:
            await db.commit()
        return deleted_photo
        
