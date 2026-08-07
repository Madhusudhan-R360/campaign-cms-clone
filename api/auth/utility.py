from passlib.context import CryptContext

from db.connection import (
    users_collection
)

from core.security import (
    create_access_token
)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

async def register_user(data):

    existing = await (
        users_collection.find_one(
            {
                "username":
                data["username"]
            }
        )
    )

    if existing:
        return {
            "success": False,
            "message":
            "User already exists"
        }

    hashed_password = (
        pwd_context.hash(
            data["password"]
        )
    )

    await users_collection.insert_one(
        {
            "username":
            data["username"],

            "password":
            hashed_password
        }
    )

    return {
        "success": True,
        "message":
        "User registered"
    }

async def login_user(data):

    user = await (
        users_collection.find_one(
            {
                "username":
                data["username"]
            }
        )
    )

    if not user:
        return {
            "success": False,
            "message":
            "Invalid credentials"
        }

    valid_password = (
        pwd_context.verify(
            data["password"],
            user["password"]
        )
    )

    if not valid_password:
        return {
            "success": False,
            "message":
            "Invalid credentials"
        }

    token = create_access_token(
        {
            "sub":
            user["username"]
        }
    )

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer"
    }
