from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger,String, TIMESTAMP, func
from db.database import Base
from typing import Optional
from datetime import datetime
class Review(Base):
    __tablename__ ='review'

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(BigInteger, nullable=False)
    trip_id:Mapped[int] = mapped_column(BigInteger, nullable=False)
    title:Mapped[str] = mapped_column(String(255),nullable=False)
    rating:Mapped[int]
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now())

# FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
# FOREIGN KEY (trip_id) REFERENCES trip(id) ON DELETE CASCADE

#like
class like(Base):
    __tablename__ ='like'
    
    user_id:Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    review_id:Mapped[int]= mapped_column(BigInteger, primary_key=True ,nullable=False)

# FOREIGN KEY (user_id) REFERENCES user(id) on delete cascade,
# FOREIGN KEY (review_id) REFERENCES review(id) on delete cascade
    

    