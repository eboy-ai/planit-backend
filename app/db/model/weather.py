from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, TEXT, String, Float
from datetime import datetime
from typing import Optional

class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True) 
    weather_info: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)  # LONGTEXT 대체
    date: Mapped[datetime] = mapped_column(nullable=False)

    # (추가) : 검색(캐싱)을 위한 컬럼
    city_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lon: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    city_weathers = relationship("CityWeather", back_populates="weather")

# CREATE TABLE weather (
#     id BIGINT PRIMARY KEY AUTO_INCREMENT,    
#     weather_info LONGTEXT,
#     date DATETIME NOT NULL,
#     city_name VARCHAR(255),
#     lat FLOAT,
#     lon FLOAT
#     -- 변경됨: 기존 trip_id, city_id FK 삭제 → 도시 연결은 city_weathers로 이관
# );