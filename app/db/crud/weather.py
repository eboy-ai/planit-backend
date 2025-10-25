from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather
from app.db.schema.weather import WeatherCreate
from sqlalchemy import select, or_, desc, func,and_
from typing import Optional
from datetime import datetime
import json
class WeatherCrud:
    @staticmethod
    async def create(db:AsyncSession,
                     weather_data:WeatherCreate):

        weather_info=json.dumps(weather_data)
        new_weather=Weather(weather_info=weather_info,created_at=datetime.utcnow())
        db.add(new_weather)
        await db.flush()
        return new_weather
    
    @staticmethod
    async def delete_old_weather(db:AsyncSession):
        pass