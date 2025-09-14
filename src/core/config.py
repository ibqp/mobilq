# HTTP configs
HTTP_TIMEOUT = 30

# Spiders configs
ELISA_CONFIG = {
    "base_url": "https://www.elisa.ee"
    , "api_endpoint": "/publicrest/manager/search"
    , "headers": {
        "User-Agent": "Mozilla/5.0"
        , "Content-Type": "application/json;charset=UTF-8"
        , "Accept": "application/json"
    }
    , "payload": {
        "categoryName": "nutitelefonid"
        , "consumerSegment": "true"
    }
    , "allowed_brands": ["Apple", "Samsung", "OnePlus", "Xiaomi", "Nothing", "Huawei", "Honor", "Poco", "Hammer"]
}

TELIA_CONFIG = {
    "base_url": "https://pood.telia.ee"
    , "api_endpoint": "/api/products/nutitelefonid/list"
    , "headers": {
        "User-Agent": "Mozilla/5.0"
        , "Content-Type": "application/json;charset=UTF-8"
        , "Accept": "application/json"
    }
    , "params": {
        "clientType": "private"
    }
    , "payload": {
        "limit": 500 # hack to get all items
    }
    , "allowed_brands": ["Apple", "Samsung", "OnePlus", "Xiaomi", "Google"]
}

TELE2_CONFIG = {
    "base_url": "https://tele2.ee"
    , "page_pool": 100 # hack to get all data at once
    , "headers": {
        "User-Agent": "Mozilla/5.0"
        , "Content-Type": "text/html; charset=utf-8"
        , "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    , "allowed_brands": ["Apple", "Samsung", "OnePlus", "Xiaomi", "Nothing", "Doro", "Nokia", "HMD"]
}
