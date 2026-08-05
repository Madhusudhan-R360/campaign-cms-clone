from datetime import datetime

import pandas as pd
from bson import ObjectId

from db.connection import (
    campaigns_collection,
    claim_codes_collection
)


async def upload_claim_codes(
    campaign_id,
    file_path
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

    df = pd.read_csv(file_path)

    expected_columns = [
        "claim_code",
        "amount",
        "email"
    ]

    if sorted(df.columns.tolist()) != sorted(expected_columns):
        return {
            "success": False,
            "message": "Invalid CSV headers"
        }

    if df["claim_code"].duplicated().any():
        return {
            "success": False,
            "message": "Duplicate claim codes in file"
        }

    if (df["amount"] <= 0).any():
        return {
            "success": False,
            "message": "Amount must be greater than zero"
        }

    records = []

    for _, row in df.iterrows():

        existing = await claim_codes_collection.find_one(
            {
                "claim_code": row["claim_code"]
            }
        )

        if existing:
            return {
                "success": False,
                "message": f"Claim code already exists: {row['claim_code']}"
            }

        records.append(
            {
                "campaign_id": ObjectId(campaign_id),
                "claim_code": row["claim_code"],
                "amount": float(row["amount"]),
                "email": row["email"],
                "active_status": True,
                "created_at": datetime.utcnow()
            }
        )

    await claim_codes_collection.insert_many(records)

    return {
        "success": True,
        "message": f"{len(records)} claim codes uploaded"
    }


async def get_claim_codes():

    claim_codes = await (
        claim_codes_collection
        .find({})
        .to_list(None)
    )

    for claim in claim_codes:
        claim["_id"] = str(claim["_id"])
        claim["campaign_id"] = str(claim["campaign_id"])

    return {
        "success": True,
        "data": claim_codes
    }


async def get_claim_code(
    claim_code_id
):

    claim = await claim_codes_collection.find_one(
        {
            "_id": ObjectId(claim_code_id)
        }
    )

    if not claim:
        return {
            "success": False,
            "message": "Claim code not found"
        }

    claim["_id"] = str(claim["_id"])
    claim["campaign_id"] = str(claim["campaign_id"])

    return {
        "success": True,
        "data": claim
    }


async def get_claim_codes_by_campaign(
    campaign_id
):

    claims = await (
        claim_codes_collection
        .find(
            {
                "campaign_id": ObjectId(campaign_id)
            }
        )
        .to_list(None)
    )

    for claim in claims:
        claim["_id"] = str(claim["_id"])
        claim["campaign_id"] = str(claim["campaign_id"])

    return {
        "success": True,
        "data": claims
    }