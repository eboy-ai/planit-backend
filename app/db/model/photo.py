from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger,String, Text, TIMESTAMP, func
from sqlalchemy.dialects.mysql import LONGBLOB
from ..database import Base
from datetime import datetime
from typing import Optional

class Photo(Base):
    __tablename__ ='photos'

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    review_id:Mapped[int] = mapped_column(BigInteger, nullable=False) #ForeignKey("review.id", ondelete="CASCADE"),
    filename:Mapped[str] = mapped_column(String(255),nullable=False)
    data:Mapped[bytes] = mapped_column(LONGBLOB,nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now()) 
    #FK, cascade 추가필요

    # FOREIGN KEY (review_id) REFERENCES review(id) ON DELETE CASCADE
    # review:Mapped["Review"]=relationship("Review", back_populates="photos")
