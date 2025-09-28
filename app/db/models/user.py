# app/db/models/user.py
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from app.db.base_class import Base # Base는 declarative_base()로 정의된 클래스라고 가정
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users" # 💡 DB에 미리 생성된 테이블 이름과 정확히 일치해야 합니다!

    # 💡 컬럼 이름, 타입 등이 DB 스키마와 정확히 일치해야 합니다!
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False) # 해시된 비밀번호
    group_id = Column(
        Integer,
        ForeignKey("groups.id"), 
        nullable=False,
        default=1 # 💡 기본값 설정 (예: 일반 사용자 그룹 ID가 1이라고 가정)
    )

    # 필요한 경우 relationship 정의
    # ...
    group = relationship("Group", back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"