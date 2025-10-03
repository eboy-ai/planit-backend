from fastapi import APIRouter, Depends, Request, Query
from app.db.database import get_db
from app.db.model import Comment
from app.db.schema.comment import CommentCreate, CommentRead, CommentUpdate
from app.services import CommentService

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/reviews/{review_id}/comments',tags=['Comments'])
#Create / 더미 user_id
async def get_user_id():
    user_id = 1
    return user_id
# 작성한 여행계획에서 id를 가져올건지 (request body)
@router.post('/', response_model=CommentRead)
async def create_comment(review_data:CommentCreate,
                        review_id:int,
                        user_id:int = Depends(get_user_id),                        
                        db:AsyncSession=Depends(get_db)):
    return await CommentService.create(db,review_data,user_id,review_id)

# 여행 계획 페이지에서 해당review_id(path param)으로 넘어오면  ++
# router = APIRouter(prefix="/reviews/{review_id}/reviews", tags=["Reviews"])

# @router.post("/", response_model=CommentRead)
# async def create_review(...):

#get_list
@router.get('/', response_model=list[CommentRead])
async def list_comments(review_id:int,
                       db:AsyncSession=Depends(get_db),
                       serach:str|None=Query(None,min_length=1),
                       limit:int = Query(10,ge=1,le=30),
                       offset:int = Query(0,ge=0)):
    return await CommentService.get_all_comment( db=db,
                                               review_id=review_id,
                                               search=serach,
                                               limit=limit,
                                               offset=offset)                                       
    
#get_comment_from_id detail
@router.get('/{comment_id}', response_model=CommentRead)
async def get_comment(comment_id:int,db:AsyncSession=Depends(get_db)):
    result = await CommentService.get_id(db,comment_id)
    add_
    return result

#update(put-restful)
@router.put('/{comment_id}', response_model=CommentRead)
async def update_comment(comment_id:int, 
                        comment:CommentUpdate,
                        user_id:int,
                        db:AsyncSession=Depends(get_db)
                        ):
    return await CommentService.update_comment_by_id(db,comment,comment_id,user_id)    

#delete
@router.delete('/delete/{comment_id}')
async def delete_comment_by_id(comment_id:int,
                               user_id:int=Depends(get_user_id),
                               db:AsyncSession=Depends(get_db)):
    db_comment = await CommentService.delete_comment_by_id(db, comment_id, user_id)
