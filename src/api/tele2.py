from src.parsers import tele2_spider
from src.models.product import Product
from typing import List, Optional, Literal
from fastapi import APIRouter, Query, HTTPException


router = APIRouter(prefix="/tele2", tags=["🤖 API"])

AllowedBrands = Literal["Apple","HMD","Nothing","Samsung","Doro","Nokia","OnePlus","Xiaomi"]

@router.get("/products", response_model=List[Product])
def get_tele2_products(brands: Optional[List[AllowedBrands]] = Query(None)):
    try:
        selected_brands = [b.strip().lower() for b in brands] if brands else None
        products = tele2_spider.run(selected_brands)
        products = Product.transform_products(products)
        return products
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
