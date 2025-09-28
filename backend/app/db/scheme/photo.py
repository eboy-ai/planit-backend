from pydantic import BaseModel, Field
from datetime import datetime, timezone

class PhotoBase(BaseModel):
    image_url: str

#Create
class PhotoCreate(PhotoBase):
    review_id: int

#Update - 사진은 파일교체 Delete+ create로 처리(비지니스로직)

#Read
class PhotoInDB(PhotoBase):
    id:int
    review_id:int
    created_at: datetime 

    class Config:
        from_attributes = True

class PhotoRead(PhotoInDB):
    pass
    