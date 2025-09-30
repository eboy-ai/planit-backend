from fastapi import APIRouter, UploadFile, File
from fastapi import  UploadFile, File, Depends
from fastapi.responses import JSONResponse

from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.model import Photo
from app.db.database import get_db
from app.services.photo import PhotoService
from app.db.schema.photo import PhotoRead
import io


router = APIRouter(prefix='/photos',tags=['Photo'])

# 사진은 api 흐름이 반대임 (router->service->crud->scheme->orm->DB)
@router.post('/upload', response_model=PhotoRead)
async def upload_photo(review_id:int, 
                       file:UploadFile = File(...),
                       db:AsyncSession=Depends(get_db)):
    return await PhotoService.create_image(db,review_id,file)