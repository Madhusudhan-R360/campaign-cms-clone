from datetime import datetime

from bson import ObjectId

from db.connection import (
    wallets_collection,
    products_collection,
    orders_collection,
    wallet_transactions_collection
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
        "status": "pending",
        "created_at": datetime.utcnow()
    }

    result = await orders_collection.insert_one(
        order
    )

    await wallet_transactions_collection.insert_one(
    {
        "claim_code":
        data["claim_code"],

        "transaction_type":
        "debit",

        "amount":
        total_amount,

        "reference":
        str(result.inserted_id),

        "description":
        f"Order redemption for "
        f"{product['name']}",

        "created_at":
        datetime.utcnow()
    }
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


async def update_order_status(
    order_id,
    status
):

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

    allowed_transitions = {
        "pending": [
            "processing",
            "cancelled",
            "failed"
        ],
        "processing": [
            "completed",
            "failed"
        ],
        "completed": [],
        "cancelled": [],
        "failed": []
    }

    current_status = order["status"]

    if status not in allowed_transitions[
        current_status
    ]:
        return {
            "success": False,
            "message": (
                f"Cannot move from "
                f"{current_status} to {status}"
            )
        }

    await orders_collection.update_one(
        {
            "_id": ObjectId(order_id)
        },
        {
            "$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            }
        }
    )

    return {
        "success": True,
        "message": f"Order moved to {status}"
    }


async def get_orders_by_status(
    status
):

    orders = await (
        orders_collection
        .find(
            {
                "status": status
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