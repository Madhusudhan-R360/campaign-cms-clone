from datetime import datetime

from bson import ObjectId

from db.connection import (
    campaigns_collection,
    claim_codes_collection,
    wallets_collection
)

async def generate_wallets(campaign_id):

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

    claim_codes = await (
        claim_codes_collection
        .find(
            {
                "campaign_id": ObjectId(campaign_id)
            }
        )
        .to_list(None)
    )

    if not claim_codes:
        return {
            "success": False,
            "message": "No claim codes found"
        }

    wallets = []

    for claim in claim_codes:

        existing_wallet = await (
            wallets_collection.find_one(
                {
                    "claim_code": claim["claim_code"]
                }
            )
        )

        if existing_wallet:
            continue

        wallets.append(
            {
                "campaign_id": claim["campaign_id"],
                "claim_code": claim["claim_code"],
                "total_balance": claim["amount"],
                "available_balance": claim["amount"],
                "consumed_balance": 0,
                "active_status": True,
                "created_at": datetime.utcnow()
            }
        )

    if wallets:
        await wallets_collection.insert_many(wallets)

    return {
        "success": True,
        "message": f"{len(wallets)} wallets generated"
    }

async def get_wallets():

    wallets = await (
        wallets_collection
        .find({})
        .to_list(None)
    )

    for wallet in wallets:
        wallet["_id"] = str(wallet["_id"])
        wallet["campaign_id"] = str(wallet["campaign_id"])

    return {
        "success": True,
        "data": wallets
    }

async def get_wallet(wallet_id):

    wallet = await wallets_collection.find_one(
        {
            "_id": ObjectId(wallet_id)
        }
    )

    if not wallet:
        return {
            "success": False,
            "message": "Wallet not found"
        }

    wallet["_id"] = str(wallet["_id"])
    wallet["campaign_id"] = str(wallet["campaign_id"])

    return {
        "success": True,
        "data": wallet
    }

async def get_wallet_by_claim_code(claim_code):

    wallet = await wallets_collection.find_one(
        {
            "claim_code": claim_code
        }
    )

    if not wallet:
        return {
            "success": False,
            "message": "Wallet not found"
        }

    wallet["_id"] = str(wallet["_id"])
    wallet["campaign_id"] = str(wallet["campaign_id"])

    return {
        "success": True,
        "data": wallet
    }