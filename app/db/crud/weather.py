from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather
from app.db.schema.weather import WeatherBase
from sqlalchemy import select, or_, desc, func,and_
from typing import Optional

class WeatherCrud:
    pass