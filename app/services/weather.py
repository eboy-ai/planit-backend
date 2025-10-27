from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather, City, CityWeather
from app.db.schema.weather import WeatherBase
from app.db.crud import WeatherCrud
from app.services import CityService
from app.routers.user import Auth_Dependency
from sqlalchemy import select
from typing import Optional
from sqlalchemy import select, or_, desc, func, delete
from app.core.settings import settings
from datetime import datetime, timedelta
import httpx
import json
class WeatherService:
    # 도시이름호출 -> 위,경도변환 -> 외부api 3시간 제한 호출 및 db저장 
    @staticmethod
    async def get_weather(db:AsyncSession,city:str):
        #1. 도시 조회 #(city=city_name)후 경도,위도 정의-외부 호출용
        result_city = await db.execute(select(City).where(City.city_name==city))
        db_city = result_city.scalars().first() #도시정보
        
        if not db_city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='도시없음')
        #새 날씨정보 호출용 위도경도
        lat, lon = db_city.lat, db_city.lon

        # 2. 해당 도시의 기존 Weather 조회
        # 기존db 반환용
        result_city_weather = await db.execute(select(CityWeather)  #result객체반환
                            .where(CityWeather.city_id==db_city.id))
           
        #요청한 도시의 반환되는 객체들중 한개만 선택
        #해당 city_weather가 존재하면 weather_id와 city_weather_id가 일치하는 row반환
        db_city_weather = result_city_weather.scalars().first()        
        print("city_weather:",db_city_weather)
        #2. db_날씨정보 저장여부
        if not db_city_weather:
            db_weather = None
        else:
            result_weather = await db.execute(select(Weather)
                                               .where(db_city_weather.weather_id==Weather.id))            
            db_weather = result_weather.scalar_one_or_none()             
        
        # 3 캐시 유효성 검사 3h       
        if db_weather and (datetime.utcnow() - db_weather.created_at) < timedelta(hours=3):                        
            weather_data = json.loads(db_weather.weather_info)
            print("db에서나간날씨정보:",type(weather_data))
            return weather_data
        
        else:
            #외부api호출 및 저장(lat:위도,lon:경도)
            url = "https://api.openweathermap.org/data/3.0/onecall"
            params = {  "lat": lat, 
                        "lon": lon,
                        "appid": settings.openweather_api_key, #민감정보 분리 .env
                        "units":'metric',  #°F -> °C
                        "lang":'kr' }
            print("현재 사용중인 API KEY:", settings.openweather_api_key)
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)            
                openweather_data=response.json()

            #호출 후 DB저장 
            new_weather = await WeatherCrud.create(db,openweather_data)
            await db.flush()
            
            if response.status_code != 200:
                # API 호출 실패 시
                raise HTTPException(status_code=response.status_code, detail=response.json())
                
            data=response.json()

        # Weather 테이블에 새 데이터 저장
        new_weather = await WeatherCrud.create(db=db, weather_data=data)
            
            #city_weather 중간테이블 저장
            db.add(CityWeather(city_id=db_city.id, weather_id=new_weather.id))       
            await db.flush()      
            print("외부api: ",type(openweather_data))
            return openweather_data
        
    #delete
    @staticmethod
    async def delete_old_weather(db:AsyncSession):
        expired_date = datetime.utcnow() - timedelta(seconds=300) #test용 30초 기존 days=30
        await db.execute(delete(Weather).where(Weather.created_at < expired_date))
        await db.flush()
        return {"msg":"30일 지난 데이터 삭제 완료"}
        
            
