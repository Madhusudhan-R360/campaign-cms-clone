from fastapi import FastAPI

from api.clients.app import router as client_router

from api.clients.app import (
    router as client_router
)

from api.accounts.app import (
    router as account_router
)

from api.products.app import (
    router as product_router
)

app = FastAPI(
    title="Campaign CMS Clone"
)

app.include_router(
    product_router,
    tags=["Products"]
)

app.include_router(
    client_router,
    tags=["Clients"]
)

app.include_router(
    client_router,
    tags=["Clients"]
)

app.include_router(
    account_router,
    tags=["Accounts"]
)
