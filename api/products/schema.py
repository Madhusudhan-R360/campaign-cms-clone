from pydantic import BaseModel
from typing import Optional


class CreateProductSchema(BaseModel):

    account_id: str

    sku: str

    name: str

    brand: str

    category: str

    price: float

    stock_count: int

    image_url: str

    active_status: bool = True


class UpdateProductSchema(BaseModel):

    sku: Optional[str] = None

    name: Optional[str] = None

    brand: Optional[str] = None

    category: Optional[str] = None

    price: Optional[float] = None

    stock_count: Optional[int] = None

    image_url: Optional[str] = None

    active_status: Optional[bool] = None