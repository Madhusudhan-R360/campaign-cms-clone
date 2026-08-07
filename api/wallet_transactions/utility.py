from bson import ObjectId

from db.connection import (
    wallet_transactions_collection
)

async def get_transactions():

    transactions = await (
        wallet_transactions_collection
        .find({})
        .to_list(None)
    )

    for transaction in transactions:

        transaction["_id"] = str(
            transaction["_id"]
        )

    return {
        "success": True,
        "data": transactions
    }

async def get_transactions_by_claim_code(
    claim_code
):

    transactions = await (
        wallet_transactions_collection
        .find(
            {
                "claim_code": claim_code
            }
        )
        .to_list(None)
    )

    for transaction in transactions:

        transaction["_id"] = str(
            transaction["_id"]
        )

    return {
        "success": True,
        "data": transactions
    }

async def get_transaction(
    transaction_id
):

    transaction = await (
        wallet_transactions_collection
        .find_one(
            {
                "_id":
                ObjectId(transaction_id)
            }
        )
    )

    if not transaction:

        return {
            "success": False,
            "message":
            "Transaction not found"
        }

    transaction["_id"] = str(
        transaction["_id"]
    )

    return {
        "success": True,
        "data": transaction
    }