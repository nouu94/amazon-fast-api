import random
import time
from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

fake = Faker()
df = pd.read_excel("spec_data_20000.xlsx")


def generate_random_product():
    random_row = df.sample(1).iloc[0]

    asin = fake.unique.bothify(text='B#########')
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


def get_insert_count_by_probability():
    chance = random.random()  # 0.0 ~ 1.0 사이 실수
    if chance < 0.01:      # 5% 확률
        return 3
    elif chance < 0.10:    # 추가 10% 확률
        return 2
    else:                  # 나머지
        return 1


def insert_multiple_data(n):
    # n개의 데이터를 동시에 삽입 (스레드 풀 사용)
    with ThreadPoolExecutor(max_workers=n) as executor: # 최대 n개의 스레드를 만들어 동시에 작업을 처리할 수 있게 합니다.
        executor.map(lambda _: insert_data(), range(n)) # executor.map(lambda _: insert_data(), range(n))


if __name__ == "__main__":
    # 20초마다 확률에 따라 1~3개의 데이터를 삽입
    while True:
        count = get_insert_count_by_probability()
        insert_multiple_data(count)
        time.sleep(20)