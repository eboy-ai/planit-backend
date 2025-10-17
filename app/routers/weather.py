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

# xlsx
@router.get("/{city_id}")
async def get_weather_by_lan(lan:float,dat:float):
    pass