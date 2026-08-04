from datetime import datetime

from bson import ObjectId

from db.connection import (
    accounts_collection,
    clients_collection
)

async def create_account(data):

    client = await clients_collection.find_one(
        {
            "_id": ObjectId(
                data["client_id"]
            )
        }
    )

    if not client:
        return {
            "success": False,
            "message": "Client not found"
        }

    data["client_id"] = ObjectId(
        data["client_id"]
    )

    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()

    result = await (
        accounts_collection.insert_one(
            data
        )
    )

    return {
        "success": True,
        "account_id": str(
            result.inserted_id
        )
    }

async def get_accounts():

    accounts = await (
        accounts_collection
        .find({})
        .to_list(None)
    )

    for account in accounts:

        account["_id"] = str(
            account["_id"]
        )

        account["client_id"] = str(
            account["client_id"]
        )

    return {
        "success": True,
        "data": accounts
    }

async def get_account(
    account_id
):

    account = await (
        accounts_collection.find_one(
            {
                "_id": ObjectId(
                    account_id
                )
            }
        )
    )

    if not account:

        return {
            "success": False,
            "message": "Account not found"
        }

    account["_id"] = str(
        account["_id"]
    )

    account["client_id"] = str(
        account["client_id"]
    )

    return {
        "success": True,
        "data": account
    }

async def get_accounts_by_client(
    client_id
):

    accounts = await (
        accounts_collection
        .find(
            {
                "client_id":
                ObjectId(client_id)
            }
        )
        .to_list(None)
    )

    for account in accounts:

        account["_id"] = str(
            account["_id"]
        )

        account["client_id"] = str(
            account["client_id"]
        )

    return {
        "success": True,
        "data": accounts
    }

async def update_account(
    account_id,
    data
):

    data["updated_at"] = (
        datetime.utcnow()
    )

    result = await (
        accounts_collection.update_one(
            {
                "_id": ObjectId(
                    account_id
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
            "message": "Account not updated"
        }

    return {
        "success": True,
        "message": "Account updated"
    }
