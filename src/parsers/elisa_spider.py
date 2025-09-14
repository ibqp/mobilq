from src.core import http
from src.models.product import Product
from src.core.config import ELISA_CONFIG
from typing import Dict, List, Optional, Any


def fetch_data(selected_brands:Optional[List[str]] = None) -> Dict[str,Any]:
    # Build URL
    base_url = ELISA_CONFIG['base_url']
    api_endpoint = ELISA_CONFIG['api_endpoint']
    url = http.build_url(base_url, api_endpoint)

    # Send request / Get response
    headers = ELISA_CONFIG['headers']
    payload = ELISA_CONFIG['payload'].copy() # avoid mutating global config
    if selected_brands:
        payload["selectedVendors"] = selected_brands # list of strings

    response = http.send_post_request(url, headers, payload)
    if not response:
        raise Exception("Failed to get response from Elisa API")

    # Return response
    raw_data = response.json()
    return raw_data


def process_data(raw_data: Dict[str,Any]) -> List[Product]:
    items_list = raw_data.get('result', [])
    products = []

    for item in items_list:
        try:
            product = Product.from_elisa_data(item)
            products.append(product)
        except Exception:
            continue

    return products


def run(selected_brands: Optional[List[str]] = None) -> List[Product]:
    raw_data = fetch_data(selected_brands)
    processed_data = process_data(raw_data)

    return processed_data
