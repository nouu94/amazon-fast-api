# db 연결 세팅

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

DATABASE_URL = "mysql+pymysql://fastapi:password@172.30.10.31:3306/shop"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 초기 테이블 생성 (필요시)
# Base.metadata.create_all(bind=engine)