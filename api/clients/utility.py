from db.connection import clients_collection
from datetime import datetime
from bson import ObjectId


async def create_client(data):

    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()

    result = await clients_collection.insert_one(data)

    return {
        "success": True,
        "client_id": str(result.inserted_id)
    }

async def get_clients():

    clients = await (
        clients_collection
        .find({})
        .to_list(length=None)
    )

    for client in clients:
        client["_id"] = str(client["_id"])

    return {
        "success": True,
        "data": clients
    }

async def get_client(client_id):

    client = await clients_collection.find_one(
        {
            "_id": ObjectId(client_id)
        }
    )

    if not client:
        return {
            "success": False,
            "message": "Client not found"
        }

    client["_id"] = str(client["_id"])

    return {
        "success": True,
        "data": client
    }

async def update_client(
    client_id,
    data
):

    data["updated_at"] = datetime.utcnow()

    result = await (
        clients_collection.update_one(
            {
                "_id": ObjectId(client_id)
            },
            {
                "$set": data
            }
        )
    )

    if result.modified_count == 0:
        return {
            "success": False,
            "message": "Client not updated"
        }

    return {
        "success": True,
        "message": "Client updated"
    }