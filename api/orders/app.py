from fastapi import APIRouter

from api.orders import utility
from api.orders.schema import CreateOrderSchema

from fastapi import Depends

from core.security import verify_token

from api.orders.schema import (
    CreateOrderSchema,
    UpdateOrderStatusSchema
)

router = APIRouter(
    dependencies=[Depends(verify_token)]
)

@router.post("/orders")
async def create_order(
    data: CreateOrderSchema
):

@router.get("/orders")
async def get_orders():
    return await utility.get_orders()


@router.get("/orders/{order_id}")
async def get_order(
    order_id: str
):
    return await utility.get_order(
        order_id
    )


@router.get(
    "/orders/claim-code/{claim_code}"
)
async def get_orders_by_claim_code(
    claim_code: str
):
    return await utility.get_orders_by_claim_code(
        claim_code
    )

@router.patch(
    "/orders/{order_id}/status"
)
async def update_order_status(
    order_id: str,
    data: UpdateOrderStatusSchema
):
    return await (
        utility.update_order_status(
            order_id,
            data.status
        )
    )

@router.get(
    "/orders/status/{status}"
)
async def get_orders_by_status(
    status: str
):
    return await (
        utility.get_orders_by_status(
            status
        )
    )

@router.post(
    "/orders/{order_id}/cancel"
)
async def cancel_order(
    order_id: str
):
    return await utility.cancel_order(
        order_id
    )