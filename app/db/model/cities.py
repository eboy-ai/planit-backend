from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger
from typing import Optional

class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True) 
    city_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  
    is_domestic: Mapped[Optional[bool]] = mapped_column(nullable=True)  

    # trip = relationship("Trip", back_populates="city")
    # place = relationship("Place", back_populates="city")

# CREATE TABLE cities (
#     id BIGINT PRIMARY KEY AUTO_INCREMENT,
#     city_name VARCHAR(255),
#     is_domestic BOOLEAN
# );