# Fast API 실행 

from app.logger import logger


from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/search-items")
def search_items_get(keywords: str = Query(...), db: Session = Depends(get_db)):

    keywords = keywords.strip('"')
    logger.info(f"검색 요청: {keywords}")

    products = db.query(Product).filter(Product.category.ilike(f"%{keywords}%")).all()
    return {
        "SearchResult": {
            "Items": [
                {
                    "ASIN": p.asin,
                    "DetailPageURL": f"https://www.amazon.com/dp/{p.asin}",
                    "ItemInfo": {
                        "Title": {
                            "DisplayValue": p.title
                        },
                        "Features": {
                            "Description": p.description
                        },
                        "Rating": {
                            "Stars": p.rating,
                            "ReviewCount": p.review_count
                        },
                        "Category": {
                            "Name": p.category
                        }
                    },
                    "Images": {
                        "Primary": {
                            "Small": {
                                "URL": p.image_url
                            }
                        }
                    },
                    "Offers": {
                        "Listings": [
                            {
                                "Price": {
                                    "Amount": p.price,
                                    "Currency": p.currency
                                }
                            }
                        ]
                    }
                } for p in products
            ]
        }
    }
