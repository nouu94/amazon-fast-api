# Amazon FastAPI Project

이 프로젝트는 FastAPI를 사용한 Amazon-style 제품 데이터 API입니다.

## 기능
- 상품 랜덤 삽입기 (엑셀 기반 스펙 활용)
- SQLite / MySQL 연동
- 자동 데이터 생성 (Faker 사용)
- FastAPI 기반 REST API 제공

## 실행 방법
```bash
uvicorn app.main:app --reload
