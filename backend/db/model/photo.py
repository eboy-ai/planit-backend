from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger,String, Text, TIMESTAMP, func
from db.database import Base

class Photo(Base):
    __tablename__ ='photo'

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    review_id:Mapped[int] = mapped_column(BigInteger, nullable=False)
    image_url:mapped_column[str] = mapped_column(String(255),nullable=False)


    # FOREIGN KEY (review_id) REFERENCES review(id) ON DELETE CASCADE