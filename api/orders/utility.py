from datetime import datetime

from bson import ObjectId

from db.connection import (
    wallets_collection,
    products_collection,
    orders_collection
)


async def create_order(data):

    wallet = await wallets_collection.find_one(
        {
            "claim_code": data["claim_code"]
        }
    )

    if not wallet:
        return {
            "success": False,
            "message": "Wallet not found"
        }

    product = await products_collection.find_one(
        {
            "_id": ObjectId(data["product_id"])
        }
    )

    if not product:
        return {
            "success": False,
            "message": "Product not found"
        }

    total_amount = (
        product["price"] *
        data["quantity"]
    )

    if wallet["available_balance"] < total_amount:
        return {
            "success": False,
            "message": "Insufficient balance"
        }

    order = {
        "claim_code": data["claim_code"],
        "product_id": product["_id"],
        "product_name": product["name"],
        "quantity": data["quantity"],
        "amount": total_amount,
        "status": "completed",
        "created_at": datetime.utcnow()
    }

    result = await orders_collection.insert_one(
        order
    )

    await wallets_collection.update_one(
        {
            "_id": wallet["_id"]
        },
        {
            "$inc": {
                "available_balance": -total_amount,
                "consumed_balance": total_amount
            }
        }
    )

    return {
        "success": True,
        "message": "Order created successfully",
        "order_id": str(result.inserted_id)
    }


async def get_orders():

    orders = await (
        orders_collection
        .find({})
        .to_list(None)
    )

    for order in orders:
        order["_id"] = str(order["_id"])
        order["product_id"] = str(
            order["product_id"]
        )

    return {
        "success": True,
        "data": orders
    }


async def get_order(order_id):

    order = await orders_collection.find_one(
        {
            "_id": ObjectId(order_id)
        }
    )

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    order["_id"] = str(order["_id"])
    order["product_id"] = str(
        order["product_id"]
    )

    return {
        "success": True,
        "data": order
    }


async def get_orders_by_claim_code(
    claim_code
):

    orders = await (
        orders_collection
        .find(
            {
                "claim_code": claim_code
            }
        )
        .to_list(None)
    )

    for order in orders:
        order["_id"] = str(order["_id"])
        order["product_id"] = str(
            order["product_id"]
        )

    return {
        "success": True,
        "data": orders
    }