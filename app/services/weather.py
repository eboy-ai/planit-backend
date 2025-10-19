from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather
from app.db.schema.weather import WeatherBase
from app.db.crud import WeatherCrud
from app.routers.user import Auth_Dependency
from sqlalchemy import select
from typing import Optional
from sqlalchemy import select, or_, desc, func
from datetime import datetime, timedelta
from app.core.settings import settings
import httpx
import json
class WeatherService:

    # 외부 api 호출 후 DB저장 기초 호출만 구현 //
    # DB 저장 후 1시간 이내 재요청시 저장된 값 DB에서 호출 추가(외부 호출 누수 방지) 
    @staticmethod
    async def get_weather_by_city(db:AsyncSession,city:str):        
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {  "q": city, 
                    "appid": settings.weather_key, # 민감정보 분리 .env
                    "units":'metric',  #°F -> °C
                    "lang":'kr' }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)            
            data = response.json()
        # 호출 후 DB저장 (수정 : 캐싱을 위해 어떤 도시의 날씨인지 저장)
        await WeatherCrud.create(db,data, city_name=city) # city_name 추가
        await db.commit()
        if response.status_code == 200:
            return data
        else:
            raise HTTPException(status_code=response.status_code, detail=data)
    
    # (추가) : 좌표(위도, 경도)로 날씨 조회
    @staticmethod
    async def get_weather_by_coords(db:AsyncSession, lat:float, lon:float):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {  "lat": lat, 
                    "lon": lon,
                    "appid": settings.weather_key, # 민감정보 분리 .env
                    "units":'metric',  #°F -> °C
                    "lang":'kr' }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)            
            data = response.json()

            # API 호출 실패 시
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=data)
            
            # API 호출 성공 시 DB 저장 (캐싱을 위해 위도, 경도 저장)
            await WeatherCrud.create(db, data, lat=lat, lon=lon)
            await db.commit()

            return data

