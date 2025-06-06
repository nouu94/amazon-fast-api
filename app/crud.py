from sqlalchemy.orm import Session
from app.models import Product

def search_products(db: Session, keyword: str):
    return db.query(Product).filter(Product.title.ilike(f"%{keyword}%")).all()