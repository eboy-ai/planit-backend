from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.model import Comment
from app.db.schema.comment import CommentCreate, CommentUpdate, CommentRead
from app.db.crud import CommentCrud
from sqlalchemy import select
from typing import Optional

class CommentService:
    #Create
    @staticmethod
    async def create(db:AsyncSession, 
                     comment_data:CommentCreate, 
                     user_id:int,
                     review_id:int):
        try:
            db_comment = await CommentCrud.create(db, comment_data,user_id,review_id)

            await db.commit()
            await db.refresh(db_comment)
            return db_comment
        except Exception:
            raise
    
    #Read    
    #trip id에 해당하는 list조회(R) vvvvvvvvv
    @staticmethod
    async def get_all_comment(db:AsyncSession,
                      review_id:int,
                      search:Optional[str]=None,
                      limit:int=10,
                      offset:int = 0):
        db_comment = await CommentCrud.get_all(db,review_id,search,limit,offset)

        return db_comment

    #Update
    @staticmethod
    async def update_comment_by_id(db:AsyncSession, comment:CommentUpdate, comment_id:int, user_id:int):
               
        db_comment = await CommentCrud.get_id(db,comment_id)
        if not db_comment:
            raise HTTPException(status_code=404, detail='리뷰가없습니다')
        #권한체크
        if db_comment.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        update_data = await CommentCrud.update_by_id(db, comment,comment_id,user_id)
        await db.commit()
        await db.refresh(update_data)
        return update_data        

    #Delete
    @staticmethod
    async def delete_commnet_by_id(db:AsyncSession, comment_id:int,user_id:int):
        db_comment = await db.execute(select(Comment).where(Comment.id==comment_id))
        comment = db_comment.scalar_one_or_none()
        

        if not comment:
            raise HTTPException(status_code=404, detail='댓글없음')

        deleted_comment = await CommentCrud.delete_by_id(db,comment_id)
        if deleted_comment:            
            await db.commit()            
        return {'detail':'댓글삭제됨'}
