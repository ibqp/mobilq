import asyncio
from src.models.product import Product
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from src.parsers import elisa_spider, telia_spider, tele2_spider
from src.core.config import ELISA_CONFIG, TELIA_CONFIG, TELE2_CONFIG



async def fetch_products(brands: Optional[List[str]] = None) -> List[Product]:

    def _filter_selected_brands(selected_brands: Optional[List[str]], allowed_brands: List[str]) -> Optional[List[str]]:
        if not selected_brands:
            return None # case when no brands selected at all

        allowed_upper = {x.upper() for x in allowed_brands} # uppercase for futher comparison
        filtered = [b.strip() for b in selected_brands if b.strip().upper() in allowed_upper]
        return filtered or None

    async def _fetch(spider, config, selected_brands: Optional[List[str]]):
        try:
            selected_brands_filtered = _filter_selected_brands(selected_brands, config["allowed_brands"])
            if not selected_brands_filtered and selected_brands:  # user picked brands, but none match
                return []

            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                return await loop.run_in_executor(executor, spider.run, selected_brands_filtered)
        except Exception:
            return []

    elisa_products, telia_products, tele2_products = await asyncio.gather(
        _fetch(spider=elisa_spider, config=ELISA_CONFIG, selected_brands=brands)
        , _fetch(spider=telia_spider, config=TELIA_CONFIG, selected_brands=brands)
        , _fetch(spider=tele2_spider, config=TELE2_CONFIG, selected_brands=brands)
    )

    return [*elisa_products, *telia_products, *tele2_products]


def pivot_products(products: List[Product]) -> List[Dict[str, Any]]:
    if not products:
        return []

    transformed_products = Product.transform_products(products)
    pivoted_products = {}

    for product in transformed_products:
        code = product.shared_code

        if code not in pivoted_products:
            pivoted_products[code] = {
                'shared_code': code
                , 'brand': product.brand
                , 'model': product.model
                , 'elisa': None
                , 'telia': None
                , 'tele2': None
            }

        # product.src = elisa, telia or tele2
        pivoted_products[code][product.src] = {
            'price': product.disc_price
            , 'url': product.full_url
        }

    result = list(pivoted_products.values())
    result.sort(key=lambda x: (x['brand'], x['model']))

    return result
