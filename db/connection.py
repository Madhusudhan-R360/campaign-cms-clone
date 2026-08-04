import motor.motor_asyncio

from db.config import settings


client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.mongo_url
)

db = client[
    settings.database_name
]


# Collections

clients_collection = db["clients"]

accounts_collection = db["accounts"]

products_collection = db["products"]

campaigns_collection = db["campaigns"]

campaign_products_link_collection = db[
    "campaign_products_link"
]

claim_codes_collection = db[
    "claim_codes"
]

wallets_collection = db[
    "wallets"
]

orders_collection = db[
    "orders"
]

order_items_collection = db[
    "order_items"
]