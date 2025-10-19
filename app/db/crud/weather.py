from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather
from app.db.schema.weather import WeatherCreate
from sqlalchemy import select, or_, desc, func,and_
from typing import Optional
from datetime import datetime, timedelta
import json
class WeatherCrud:
    @staticmethod
    async def create(db: AsyncSession,
                        weather_data: dict,
                        city_name: Optional[str] = None,
                        lat: Optional[float] = None,
                        lon: Optional[float] = None
                    ):

        weather_info=json.dumps(weather_data)
        new_weather = Weather(
            weather_info = weather_info,
            date = datetime.utcnow(),
            city_name = city_name,
            lat = lat,
            lon = lon
        )
        db.add(new_weather)
        await db.flush()
        return new_weather
    
    # (추가) : 좌표(위도, 경도) 기준으로 최근 1시간 이내의 날씨 데이터 조회
    @staticmethod
    async def get_recent_weather_by_coords(db: AsyncSession, lat: float, lon: float) -> Optional[Weather]:

        # 1시간 전 시간 계산
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        
        # 위도/경도가 비슷하고 (소수점 2자리까지), 최근 1시간 이내인 데이터 조회
        stmt = select(Weather).where(
            Weather.lat.isnot(None),
            Weather.lon.isnot(None),
            func.round(Weather.lat, 2) == round(lat, 2), # 근사치 검색
            func.round(Weather.lon, 2) == round(lon, 2), # 근사치 검색
            Weather.date >= one_hour_ago
        ).order_by(desc(Weather.date)).limit(1)
        
        result = await db.execute(stmt)
        weather = result.scalars().first()
        return weather