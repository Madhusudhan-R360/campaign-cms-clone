from datetime import datetime

from bson import ObjectId

from db.connection import (
    campaigns_collection,
    campaign_products_link_collection,
    products_collection,
    accounts_collection
)

async def create_campaign(data):

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

    data["account_id"] = ObjectId(
        data["account_id"]
    )

    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()

    result = await campaigns_collection.insert_one(
        data
    )

    return {
        "success": True,
        "campaign_id": str(
            result.inserted_id
        )
    }

async def get_campaigns():

    campaigns = await (
        campaigns_collection
        .find({})
        .to_list(None)
    )

    for campaign in campaigns:

        campaign["_id"] = str(
            campaign["_id"]
        )

        campaign["account_id"] = str(
            campaign["account_id"]
        )

    return {
        "success": True,
        "data": campaigns
    }

async def get_campaign(campaign_id):

    campaign = await campaigns_collection.find_one(
        {
            "_id": ObjectId(campaign_id)
        }
    )

    if not campaign:

        return {
            "success": False,
            "message": "Campaign not found"
        }

    campaign["_id"] = str(
        campaign["_id"]
    )

    campaign["account_id"] = str(
        campaign["account_id"]
    )

    return {
        "success": True,
        "data": campaign
    }

async def update_campaign(
    campaign_id,
    data
):

    data["updated_at"] = datetime.utcnow()

    result = await (
        campaigns_collection.update_one(
            {
                "_id": ObjectId(
                    campaign_id
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
            "message": "Campaign not updated"
        }

    return {
        "success": True,
        "message": "Campaign updated"
    }

async def add_product_to_campaign(
    campaign_id,
    data
):

    campaign = await campaigns_collection.find_one(
        {
            "_id": ObjectId(campaign_id)
        }
    )

    if not campaign:

        return {
            "success": False,
            "message": "Campaign not found"
        }

    product = await products_collection.find_one(
        {
            "_id": ObjectId(
                data["product_id"]
            )
        }
    )

    if not product:

        return {
            "success": False,
            "message": "Product not found"
        }

    existing_link = await (
        campaign_products_link_collection
        .find_one(
            {
                "campaign_id": ObjectId(
                    campaign_id
                ),
                "product_id": ObjectId(
                    data["product_id"]
                )
            }
        )
    )

    if existing_link:

        return {
            "success": False,
            "message": "Product already linked"
        }

    link_data = {

        "campaign_id": ObjectId(
            campaign_id
        ),

        "product_id": ObjectId(
            data["product_id"]
        ),

        "min_qty": data["min_qty"],

        "max_qty": data["max_qty"],

        "created_at": datetime.utcnow()
    }

    await (
        campaign_products_link_collection
        .insert_one(link_data)
    )

    return {
        "success": True,
        "message": "Product linked"
    }

async def get_campaign_products(
    campaign_id
):

    links = await (
        campaign_products_link_collection
        .find(
            {
                "campaign_id":
                ObjectId(campaign_id)
            }
        )
        .to_list(None)
    )

    results = []

    for link in links:

        product = await (
            products_collection.find_one(
                {
                    "_id": link["product_id"]
                }
            )
        )

        if product:

            results.append({
                "product_id":
                str(product["_id"]),

                "sku":
                product["sku"],

                "name":
                product["name"],

                "price":
                product["price"],

                "min_qty":
                link["min_qty"],

                "max_qty":
                link["max_qty"]
            })

    return {
        "success": True,
        "data": results
    }