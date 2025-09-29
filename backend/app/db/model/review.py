from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger,String, Text, TIMESTAMP, func, ForeignKey
from ..database import Base
from typing import Optional
from datetime import datetime

class Review(Base):
    __tablename__ ='review'

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(BigInteger, nullable=False)
    trip_id:Mapped[int] = mapped_column(BigInteger, nullable=False)
    title:Mapped[str] = mapped_column(String(255),nullable=False)
    content:Mapped[str] = mapped_column(Text, nullable=False)
    rating:Mapped[int]
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now())

    # # FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    # users:Mapped["User"]=relationship("User", back_populates="review")
    # # FOREIGN KEY (trip_id) REFERENCES trip(id) ON DELETE CASCADE
    # trip:Mapped["Trip"]=relationship("Trip", back_populates="review")

#like
class Like(Base):
    __tablename__ ='likes'
    # primary key(user_id,review_id) 복합키 - 좋아요 중복방지
    user_id:Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    review_id:Mapped[int]= mapped_column(BigInteger, primary_key=True ,nullable=False)

    # # FOREIGN KEY (user_id) REFERENCES users(id) on delete cascade,
    # users:Mapped["User"]=relationship("User", back_populates="likes")
    # # FOREIGN KEY (review_id) REFERENCES review(id) on delete cascade
    # review:Mapped["Review"]=relationship("Review", back_populates="likes")
        

    