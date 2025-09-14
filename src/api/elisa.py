from src.parsers import elisa_spider
from src.models.product import Product
from typing import List, Optional, Literal
from fastapi import APIRouter, Query, HTTPException


router = APIRouter(prefix="/elisa", tags=["🤖 API"])

AllowedBrands = Literal["Apple","Huawei","OnePlus","Samsung","Hammer","Honor","Nothing","Poco","Xiaomi"]

@router.get("/products", response_model=List[Product])
def get_elisa_products(brands: Optional[List[AllowedBrands]] = Query(None)):
    try:
        selected_brands = [b.strip().upper() for b in brands] if brands else None
        products = elisa_spider.run(selected_brands)
        products = Product.transform_products(products)
        return products
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
