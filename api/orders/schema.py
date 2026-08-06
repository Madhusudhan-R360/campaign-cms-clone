from pydantic import BaseModel


class CreateOrderSchema(BaseModel):

    claim_code: str

    product_id: str

    quantity: int = 1