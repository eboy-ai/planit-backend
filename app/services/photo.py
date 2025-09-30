from fastapi import HTTPException,status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.model import Photo
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
                                          data=contents)
        await db.commit()
        await db.refresh(db_photo)        
        return db_photo