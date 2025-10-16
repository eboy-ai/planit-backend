from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import Weather
from app.db.schema.weather import WeatherBase
from app.db.crud import WeatherCrud
from app.routers.user import Auth_Dependency
from sqlalchemy import select
from typing import Optional
from sqlalchemy import select, or_, desc, func

class WeatherService:
    pass