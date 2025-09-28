# app/db/base_class.py
from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase # SQLAlchemy 2.0+ 스타일 사용

# 모든 ORM 모델이 상속받을 Base 클래스를 정의합니다.
class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        # 예시: 클래스 이름을 snake_case로 변환하여 테이블 이름으로 사용 (선택 사항)
        import re
        name = cls.__name__
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    # 모든 테이블에 공통으로 필요한 컬럼을 여기에 정의할 수 있습니다.
    id: Any 
    
    pass