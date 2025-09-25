from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True) #index는 자주쓰이는칼럼에
    name = Column(String(50), nullable=False)