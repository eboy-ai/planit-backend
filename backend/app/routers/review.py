from fastapi import APIRouter, Depends
from db.database import get_db
from db.models import Review

from sqlalchemy.ext.asyncio import AsyncSession



router = APIRouter(prefix='/reviews',tags=['Review'])
#Create
@router.post('/')
async def create_review():
    pass
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
@router.delete('/delete//{review_id}')
async def delete_review_by_id():
    pass