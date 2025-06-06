# FastAPI + DB + 자동 데이터 생성 + Mock API 제공

# 기능별 구성
# DB 구성 (ex: mysql)
# → 상품 데이터, 판매 시간, 가격 정보 저장
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True) # 상품 id
    asin = Column(String(20), unique=True, nullable=False) # ASIN (Amazon Standard Identification Number)
    title = Column(String(255), nullable=False) # 상품 타이틀
    price = Column(Float, nullable=False) # 상품 가격
    currency = Column(String(10), default="USD") # 통화 단위
    store = Column(String(100)) # 판매처
    created_at = Column(DateTime, default=datetime.utcnow) # 데이터 생성 시간
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # 데이터 수정 시간
    description = Column(String(500), nullable=True) # 상품 설명
    image_url = Column(String(255), nullable=True) # 상품 이미지 URL
    category = Column(String(100), nullable=True) # 상품 카테고리
    stock = Column(Integer, default=0) # 재고 수량
    rating = Column(Float, default=0.0) # 상품 평점
    review_count = Column(Integer, default=0) # 상품 리뷰 수
    
