import requests
from src.core.config import HTTP_TIMEOUT
from urllib.parse import urljoin, urlencode
from typing import Optional, Any, Union, List, Tuple, Dict


def build_url(
    base_url: str
    , endpoint: str
    , params: Optional[Union[Dict[str,Any], List[Tuple[str, Any]]]] = None
) -> str:
    url = urljoin(base_url, endpoint)
    if params:
        query_string = urlencode(params, doseq=True)
        url = f"{url}?{query_string}"
    return url

def send_get_request(
    url:str
    , headers: Optional[Dict[str, str]] = None
) -> Optional[requests.Response]:
    try:
        response = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
        response.raise_for_status()
        return response
    except Exception:
        raise

def send_post_request(
    url:str
    , headers:Dict[str, str]
    , payload:Dict[str, Any]
) -> Optional[requests.Response]:
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=HTTP_TIMEOUT)
        response.raise_for_status()
        return response
    except Exception:
        raise
