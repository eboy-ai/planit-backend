from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather, City
from app.db.schema.weather import WeatherBase
from app.db.crud import WeatherCrud
from app.services import CityService
from app.routers.user import Auth_Dependency
from sqlalchemy import select
from typing import Optional
from sqlalchemy import select, or_, desc, func
from app.core.settings import settings
from datetime import datetime, timedelta
import httpx
import json
class WeatherService:
    #외부 api 호출 후 DB저장 기초호출만구현//
    #  DB저장후 1시간 이내 재요청시 저장된값 DB에서 호출추가(외부호출누수 방지) 
    #1도시조회
    #2db캐시확인 조건분기(2h이상 2h 미만)
    #3 city_name / get city_id join / 외부 api호출
    @staticmethod
    async def get_weather(db:AsyncSession,city:str):
        #도시 조회
        result = await db.execute(select(City).where(City.city_name==city))
        db_city = result.scalars().first() #도시객체

        if not db_city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='도시없음')
        lat = db_city.lat
        lon = db_city.lon



        #외부api호출 및 저장(lat,lon)
        url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {  "lat": lat, 
                    "lon": lon,
                    "appid": settings.weather_key, #민감정보 분리 .env
                    "units":'metric',  #°F -> °C
                    "lang":'kr' }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)            
            data=response.json()

        #호출 후 DB저장
        await WeatherCrud.create(db,data)
        await db.commit()
        if response:
            return data
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
