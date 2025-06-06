import random
import time
from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import logging
import random 
import pandas as pd 

fake = Faker()

# pandas를 사용하여 엑셀 파일에서 데이터를 읽어옵니다.
# critical : 엑셀 파일은 'spec_data_20000.xlsx'로 가정하지만 추후 장비의 스펙 공부 후 데이터를 다시 만들어야 됩니다.
df = pd.read_excel("spec_data_20000.xlsx")


# Faker를 사용하여 랜덤한 상품 데이터를 생성하는 함수
# 이 함수는 ASIN, 제목, 가격, 통화, 스토어, 설명, 이미지 URL, 카테고리, 재고, 평점 및 리뷰 수를 포함합니다.
# 생성된 데이터는 Product 모델에 맞춰져 있으며, 생성 및 업데이트 시간은 현재 UTC 시간으로 설정됩니다.
def generate_random_product():

    # 랜덤으로 행을 선택
    random_row = df.sample(1).iloc[0]


    asin = fake.unique.bothify(text='B#########')  # warning : 랜덤 ASIN 중복 가능성 있음!
    title = f"{random_row['Vendor']} {random_row['Model']} {fake.word().capitalize()}"
    price = round(random.uniform(200.0, 4000.0), 2)
    currency = "USD"
    store = fake.company()
    description = random_row['Spec']
    image_url = f"https://example.com/image/{asin}.jpg"
    category = random_row['Type']
    stock = random.randint(0, 100)
    rating = round(random.uniform(2, 5), 1)
    review_count = random.randint(0, 1000)

    return Product(
        asin=asin,
        title=title,
        price=price,
        currency=currency,
        store=store,
        description=description,
        image_url=image_url,
        category=category,
        stock=stock,
        rating=rating,
        review_count=review_count,
        created_at=datetime.now(ZoneInfo("Asia/Seoul")),
        updated_at=datetime.now(ZoneInfo("Asia/Seoul")),
    )


def insert_data():
    db: Session = SessionLocal()
    try:
        product = generate_random_product()
        db.add(product)
        db.commit()
        print(f"[{datetime.utcnow()}] Inserted: {product.asin}")
    except Exception as e:
        logging.exception("Error inserting data")
        print("Error:", e)
        db.rollback()
    finally:
        db.close()



if __name__ == "__main__":
    while True:
        insert_data()
        time.sleep(20)  # 60초 간격으로 삽입