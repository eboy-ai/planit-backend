from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger,String, Text, TIMESTAMP, func
from ..database import Base
from typing import Optional
from datetime import datetime

class Comment(Base):
    __tablename__ = 'comments'

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(BigInteger, nullable=False)
    review_id:Mapped[int] = mapped_column(BigInteger, nullable=False)
    content:Mapped[str] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now())

# # FOREIGN KEY (user_id) REFERENCES users(id) on delete cascade,
# users:Mapped["User"]=relationship("User", back_populates="comments")
# # FOREIGN KEY (review_id) REFERENCES review(id) on delete cascade
# review:Mapped["Review"]=relationship("Review", back_populates="comments")