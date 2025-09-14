import re
from src.core import http
from src.models.product import Product
from src.core.config import TELE2_CONFIG
from typing import Dict, List, Optional, Any


def fetch_data(selected_brands: Optional[List[str]] = None) -> Dict[str, Any]:
    def _get_latest_build_id() -> str:
        url = "https://tele2.ee/pood/mobiiltelefonid/"
        response = http.send_get_request(url)
        if not response:
            return 'build53789' # Failed to fetch data. Returning dummy build: build53789

        html = response.text
        match = re.search(r'/_next/static/(\w+)/_buildManifest.js', html)
        if not match:
            return 'build53789' # Failed to match BuildID. Returning dummy build: build53789

        return match.group(1)

    # Build URL
    base_url = TELE2_CONFIG['base_url']
    page_pool = TELE2_CONFIG['page_pool']
    latest_build_id = _get_latest_build_id()

    if selected_brands:
        selected_brands_str = ','.join(selected_brands) # concatenate list to string
        api_endpoint=f'/_next/data/{latest_build_id}/et/pood/mobiiltelefonid/is_available_on_eshop/1/brand/{selected_brands_str}/page/{page_pool}.json'
    else:
        api_endpoint=f'/_next/data/{latest_build_id}/et/pood/mobiiltelefonid/is_available_on_eshop/1/page/{page_pool}.json'

    url = http.build_url(base_url,api_endpoint) # url contains only phones available on e-shop


    # Send request / Get response
    headers = TELE2_CONFIG['headers']
    response = http.send_get_request(url, headers)
    if not response:
        raise Exception("Failed to get response from Tele2 API")

    # Return response
    raw_data = response.json().get('pageProps', {}).get('initialApolloState', {})
    return raw_data

def process_data(raw_data: Dict[str, Any]) -> List[Product]:
    products = []

    for key, item in raw_data.items():
        try:
            if key.startswith("ConfigurableProduct"):
                product = Product.from_tele2_data(item)
                products.append(product)
        except Exception:
            continue

    return products

def run(selected_brands: Optional[List[str]] = None) -> List[Product]:
    raw_data = fetch_data(selected_brands)
    processed_data = process_data(raw_data)

    return processed_data
