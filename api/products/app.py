from fastapi import APIRouter, Depends

from api.products.schema import (
    CreateProductSchema,
    UpdateProductSchema
)
from core.security import verify_token
from api.products import utility

router = APIRouter(
    dependencies=[Depends(verify_token)]
)

@router.post("/products")
async def create_product(
    data: CreateProductSchema
):
    return await utility.create_product(
        data.model_dump()
    )


@router.get("/products")
async def get_products():
    return await utility.get_products()


@router.get("/products/{product_id}")
async def get_product(
    product_id: str
):
    return await utility.get_product(
        product_id
    )


@router.get(
    "/products/account/{account_id}"
)
async def get_products_by_account(
    account_id: str
):
    return await utility.get_products_by_account(
        account_id
    )


@router.put(
    "/products/{product_id}"
)
async def update_product(
    product_id: str,
    data: UpdateProductSchema
):

    payload = {
        k: v
        for k, v in data.model_dump().items()
        if v is not None
    }

    return await utility.update_product(
        product_id,
        payload
    )