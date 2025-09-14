from typing import Optional, List
from src.models.product import Product
from src.services import product_service
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Query, HTTPException


router = APIRouter(tags=["🌐 WEB"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/search", response_class=HTMLResponse)
async def search_products(request: Request, brands: Optional[List[str]] = Query(default=None)):
    try:
        # Fetch products
        selected_brands = brands if brands else None
        all_products = await product_service.fetch_products(selected_brands)

        # Transform products
        all_products = Product.transform_products(all_products)

        # Pivot products
        pivoted_list = product_service.pivot_products(all_products)

        return templates.TemplateResponse(
            "results.html"
            , {
                "request": request
                , "products": pivoted_list
                , "selected_brands": selected_brands
                , "total_products": len(all_products)
            }
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong during search")
