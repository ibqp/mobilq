from src.core import http
from src.models.product import Product
from src.core.config import TELIA_CONFIG
from typing import Dict, List, Optional, Any


def fetch_data(selected_brands:Optional[List[str]] = None) -> Dict[str,Any]:
    # Build URL
    base_url = TELIA_CONFIG['base_url']
    api_endpoint = TELIA_CONFIG['api_endpoint']
    params = TELIA_CONFIG['params']
    url = http.build_url(base_url, api_endpoint, params)

    # Send request / Get response
    headers = TELIA_CONFIG['headers']
    payload = TELIA_CONFIG['payload'].copy() # avoid mutating global config
    if selected_brands:
        payload["manufacturers"] = selected_brands # list of strings

    response = http.send_post_request(url, headers, payload)
    if not response:
        raise Exception("Failed to get response from Telia API")

    # Return response
    raw_data = response.json()
    return raw_data

def process_data(raw_data: Dict[str,Any]) -> List[Product]:
    items_list = raw_data.get('products', [])
    products = []

    for item in items_list:
        try:
            product = Product.from_telia_data(item)
            products.append(product)
        except Exception:
            continue

    return products

def run(selected_brands: Optional[List[str]] = None) -> List[Product]:
    raw_data = fetch_data(selected_brands)
    processed_data = process_data(raw_data)

    return processed_data
