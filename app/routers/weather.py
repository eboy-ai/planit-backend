from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
#trip
from app.services.trip_service import TripService
from app.db.schema.trip import TripCreate, TripUpdate, TripInDB
from app.db.schema.trip_day import TripDayCreate, TripDayInDB
from app.db.schema.schedule import ScheduleCreate, ScheduleUpdate, ScheduleInDB
from app.db.schema.checklist_item import ChecklistItemCreate, ChecklistItemUpdate, ChecklistItemInDB
#city
from app.services.city_service import CityService
from app.db.schema.cities import CityCreate, CityInDB
from app.db.schema.places import PlaceCreate, PlaceInDB

from app.core.settings import settings

router = APIRouter(prefix="/weather", tags=["Weather"])

#도시이름으로 외부api 조회
@router.get("/")
async def get_weather_by_city_url(city:str):
    pass

@router.get("/{city_id}")
async def get_weather_by_lan(lan:float,dat:float):
    pass