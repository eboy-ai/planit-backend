from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather
from app.db.schema.weather import WeatherBase
from app.db.crud import WeatherCrud
from app.routers.user import Auth_Dependency
from sqlalchemy import select
from typing import Optional
from sqlalchemy import select, or_, desc, func
from app.core.settings import settings
import httpx
import json
class WeatherService:
    #외부 api 호출 후 DB저장 기초호출만구현//
    #  DB저장후 1시간 이내 재요청시 저장된값 DB에서 호출추가(외부호출누수 방지) 
    @staticmethod
    async def get_weather(db:AsyncSession,city:str):        
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {  "q": city, 
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
