from src.parsers import telia_spider
from src.models.product import Product
from typing import List, Optional, Literal
from fastapi import APIRouter, Query, HTTPException


router = APIRouter(prefix="/telia", tags=["🤖 API"])

AllowedBrands = Literal["Apple","Google","OnePlus","Samsung","Xiaomi"]

@router.get("/products", response_model=List[Product])
def get_telia_products(brands: Optional[List[AllowedBrands]] = Query(None)):
    try:
        selected_brands = [b.strip() for b in brands] if brands else None
        products = telia_spider.run(selected_brands)
        products = Product.transform_products(products)
        return products
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
