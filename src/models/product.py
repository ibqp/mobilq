import re
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any


class Product(BaseModel):
    id: str = Field(...)
    src: str = Field(...)
    brand: str = Field(...)
    model: str = Field(...)
    full_price: float = Field(...)
    disc_price: float = Field(...)
    full_url: str = Field(...)
    shared_code: Optional[str] = None # calcualted field

    @classmethod
    def transform_products(cls, products: List["Product"]) -> List["Product"]:
        for p in products:
            # Replace zero prices
            if p.full_price == 0:
                p.full_price = p.disc_price

            # Generate shared code, clean model name
            if p.brand in p.model:
                shared_code = p.model.replace(" ", "")
                p.model = p.model.replace(p.brand, "").strip()
            else:
                shared_code = (p.brand + p.model).replace(" ", "")

            # Remove whitespace before GB or TB
            p.model = re.sub(r'\s+(GB|TB)$', r'\1', p.model)

            # Add shared code to a model
            setattr(p, "shared_code", shared_code)

        return products

    @classmethod
    def from_elisa_data(cls, item: Dict[str,Any]) -> "Product":
        full_url = f"https://www.elisa.ee/seadmed/eraklient/nutitelefonid/{item.get('seoURL','')}"
        return cls(
            id=str(item.get("id",""))
            , src="elisa"
            , brand=item.get("vendor", "").upper()
            , model=item.get("model", "").upper()
            , full_price=float(item.get("price", 0))
            , disc_price=float(item.get("customerPrice", 0))
            , full_url=full_url
        )

    @classmethod
    def from_tele2_data(cls, item: Dict[str,Any]) -> "Product":
        full_url = f"https://tele2.ee/{item.get('product_url_full','')}"
        return cls(
            id=str(item.get("id",""))
            , src="tele2"
            , brand=item.get("brand_label","").upper()
            , model=item.get("name","").upper()
            , full_price=float(item.get("price",{}).get("price",0))
            , disc_price=float(item.get("price",{}).get("specialPrice",0))
            , full_url=full_url
        )

    @classmethod
    def from_telia_data(cls, item: Dict[str,Any]) -> "Product":
        full_url = f"https://pood.telia.ee{item.get('url','')}"
        return cls(
            id=str(item.get("productCode",""))
            , src="telia"
            , brand=item.get("manufacturer","").upper()
            , model=item.get("name",{}).get("et","").upper()
            , full_price=float((item.get("prices",{}).get("previouslyBestPrice") or {}).get("amount",0))
            , disc_price=float((item.get("prices",{}).get("currentPrice") or {}).get("amount",0))
            , full_url=full_url
        )
