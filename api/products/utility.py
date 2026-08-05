from datetime import datetime
from bson import ObjectId

from db.connection import (
    products_collection,
    accounts_collection
)

async def create_product(data):

    account = await accounts_collection.find_one(
        {
            "_id": ObjectId(
                data["account_id"]
            )
        }
    )

    if not account:

        return {
            "success": False,
            "message": "Account not found"
        }

    sku_exists = await products_collection.find_one(
        {
            "sku": data["sku"]
        }
    )

    if sku_exists:

        return {
            "success": False,
            "message": "SKU already exists"
        }

    data["account_id"] = ObjectId(
        data["account_id"]
    )

    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()

    result = await products_collection.insert_one(
        data
    )

    return {
        "success": True,
        "product_id": str(
            result.inserted_id
        )
    }

async def get_products():

    products = await (
        products_collection
        .find({})
        .to_list(None)
    )

    for product in products:

        product["_id"] = str(
            product["_id"]
        )

        product["account_id"] = str(
            product["account_id"]
        )

    return {
        "success": True,
        "data": products
    }

async def get_product(product_id):

    product = await products_collection.find_one(
        {
            "_id": ObjectId(product_id)
        }
    )

    if not product:

        return {
            "success": False,
            "message": "Product not found"
        }

    product["_id"] = str(
        product["_id"]
    )

    product["account_id"] = str(
        product["account_id"]
    )

    return {
        "success": True,
        "data": product
    }

async def get_products_by_account(
    account_id
):

    products = await (
        products_collection
        .find(
            {
                "account_id":
                ObjectId(account_id)
            }
        )
        .to_list(None)
    )

    for product in products:

        product["_id"] = str(
            product["_id"]
        )

        product["account_id"] = str(
            product["account_id"]
        )

    return {
        "success": True,
        "data": products
    }

async def update_product(
    product_id,
    data
):

    data["updated_at"] = datetime.utcnow()

    result = await (
        products_collection.update_one(
            {
                "_id": ObjectId(
                    product_id
                )
            },
            {
                "$set": data
            }
        )
    )

    if result.modified_count == 0:

        return {
            "success": False,
            "message": "Product not updated"
        }

    return {
        "success": True,
        "message": "Product updated"
    }
