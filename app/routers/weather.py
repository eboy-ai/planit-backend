from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db

from app.services.weather import WeatherService

from app.core.settings import settings


router = APIRouter(prefix="/weather", tags=["Weather"])

#도시이름으로 외부api 조회 및 DB저장
@router.get("/",description='Get and Create Weather')
async def get_weather_by_city_url(city:str,db:AsyncSession=Depends(get_db)):
    return await WeatherService.get_weather(db,city)

# 30일 지난 데이터 삭제 (관리자 의존성 추가 가능) Weather.date기준 30일
@router.get("/delete-old-weather", description="30일지난 데이터 삭제")
async def cleanup_weather(db:AsyncSession=Depends(get_db)):
    result = await WeatherService.delete_old_weather(db)
    return result