from pydantic import BaseModel
from typing import Optional

class CityBase(BaseModel):
    city_name: Optional[str] = None
    is_domestic: Optional[bool] = None

class CityCreate(CityBase):
    city_name: str # 생성 시 도시 이름 필수

class CityInDB(CityBase):
    id: int

    class Config:
        from_attributes = True