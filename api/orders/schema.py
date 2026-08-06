from pydantic import BaseModel
from typing import Literal

class CreateOrderSchema(BaseModel):

    claim_code: str

    product_id: str

    quantity: int = 1

class UpdateOrderStatusSchema(BaseModel):

    status: Literal[
        "processing",
        "completed",
        "cancelled",
        "failed"
    ]