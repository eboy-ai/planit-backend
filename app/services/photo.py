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
    
    #사진 한개(대표이미지용) 조회
    @staticmethod
    async def get_photo(db:AsyncSession,review_id:int,photo_id:int):        
        query = select(Photo).where(Review.id == review_id,
                                    Photo.id == photo_id)
        #예외처리
        result = await db.execute(query)
        db_photo = result.scalar_one_or_none()
        return db_photo
    
    # #원본이미지 조회
    # @staticmethod
    # async def get_image_raw(db:AsyncSession, review_id:int, photo_id:int):
    #     query = select(Photo).where(Review.id == review_id,
    #                                 Photo.id == photo_id)