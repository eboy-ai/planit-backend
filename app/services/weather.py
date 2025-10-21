from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather, City, CityWeather
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
        db_city = result.scalars().first() #도시정보

        if not db_city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='도시없음')
        lat = db_city.lat
        lon = db_city.lon

        # 해당 도시의 기존 Weather 조회
        # if CityWeather.
        query1 = await db.execute(select(CityWeather.weather_id)
                            .where(CityWeather.city_id==db_city.id))
        db_city_weather_id = query1
        if db_city_weather_id:
            query2 = await db.execute(select(Weather).where(Weather.id == db_city.id))
            db_weather = query2.scalars().first()

        # 3 캐시 유효성 검사
        if db_weather and (datetime.utcnow() - db_weather.date) < timedelta(hours=3):
            return json.loads(db_weather.weather_info)
        
        else:
            #외부api호출 및 저장(lat,lon)
            url = "https://api.openweathermap.org/data/3.0/onecall"
            params = {  "lat": lat, 
                        "lon": lon,
                        "appid": settings.weather_key, #민감정보 분리 .env
                        "units":'metric',  #°F -> °C
                        "lang":'kr' }
            print("현재 사용중인 API KEY:", settings.weather_key)
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)            
                data=response.json()

            #호출 후 DB저장 or update
            new_weather = await WeatherCrud.create(db,data)
            await db.flush()
            await db.refresh(new_weather)
            if response.status_code != 200:
                raise HTTPException(status_code=502, detail={response.text})
            
            #city_weather 중간테이블 저장
            db.add(CityWeather(city_id=db_city.id, weather_id=new_weather.id))       
            await db.flush()        

            return data
            
