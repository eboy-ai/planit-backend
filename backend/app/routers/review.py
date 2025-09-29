from fastapi import APIRouter, Depends, Request
from app.db.database import get_db
from app.db.model import Review
from app.db.schema.review import ReviewCreate, ReviewRead, ReviewUpdate
from app.services import ReviewService

from sqlalchemy.ext.asyncio import AsyncSession



router = APIRouter(prefix='/reviews',tags=['Review'])
#Create
async def get_user_id():
    user_id = 1
    return user_id
# 작성한 여행계획에서 id를 가져올건지 (request body)
@router.post('/', response_model=ReviewRead)
async def create_review(review_data:ReviewCreate,
                        trip_id:int,
                        user_id:int = Depends(get_user_id),                        
                        db:AsyncSession=Depends(get_db)):
    return await ReviewService.create(db,review_data,user_id,trip_id)

# 여행 계획 페이지에서 해당trip_id(path param)으로 넘어오면  ++
# router = APIRouter(prefix="/trips/{trip_id}/reviews", tags=["Reviews"])

# @router.post("/", response_model=ReviewRead)
# async def create_review(...):

#get_list
@router.get('/')
async def list_reviews():
    pass

#get_id detail
@router.get('/{review_id}')
async def read_review():
    pass

#update
@router.put('/edit/{review_id}')
async def update_review():
    pass

#delete
@router.delete('/delete/{review_id}')
async def delete_review_by_id():
    pass