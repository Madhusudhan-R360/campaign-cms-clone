from fastapi import APIRouter, Depends
from core.security import verify_token
from api.wallets import utility

router = APIRouter(
    dependencies=[Depends(verify_token)]
)

@router.post("/wallets/generate/{campaign_id}")
async def generate_wallets(
    campaign_id: str
):
    return await utility.generate_wallets(
        campaign_id
    )

@router.get("/wallets")
async def get_wallets():
    return await utility.get_wallets()

@router.get("/wallets/{wallet_id}")
async def get_wallet(
    wallet_id: str
):
    return await utility.get_wallet(
        wallet_id
    )

@router.get(
    "/wallets/claim-code/{claim_code}"
)
async def get_wallet_by_claim_code(
    claim_code: str
):
    return await utility.get_wallet_by_claim_code(
        claim_code
    )