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

from api.campaigns.app import (
    router as campaign_router
)

from api.claim_codes.app import (
    router as claim_code_router
)

from api.wallets.app import (
    router as wallet_router
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

app.include_router(
    campaign_router,
    tags=["Campaigns"]
)

app.include_router(
    claim_code_router,
    tags=["Claim Codes"]
)

app.include_router(
    wallet_router,
    tags=["Wallets"]
)