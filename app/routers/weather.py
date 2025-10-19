from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db

from app.services.weather import WeatherService

from app.core.settings import settings


router = APIRouter(prefix="/weather", tags=["Weather"])

# 도시이름으로 외부api 조회 및 DB저장
@router.get("/",description='Get and Create Weather')
async def get_weather_by_city_url(city:str,db:AsyncSession=Depends(get_db)):
    return await WeatherService.get_weather_by_city(db,city)

# (수정) 현재 위치(위도, 경도)로 날씨 조회
@router.get("/current", description="Get Current Weather by Coordinates")
async def get_weather_by_coords_url(
    lat: float = Query(..., description="Latitude (위도)"),
    lon: float = Query(..., description="Longitude (경도)"),
    db: AsyncSession = Depends(get_db)
):
    # 서비스에도 새로운 함수 (get_weather_by_coords)를 만들어 호출한다.
    return await WeatherService.get_weather_by_coords(db, lat=lat, lon=lon)