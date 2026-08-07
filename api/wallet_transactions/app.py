from fastapi import APIRouter

from api.wallet_transactions import utility

router = APIRouter()

@router.get(
    "/wallet-transactions"
)
async def get_transactions():
    return await utility.get_transactions()


@router.get(
    "/wallet-transactions/{transaction_id}"
)
async def get_transaction(
    transaction_id: str
):
    return await utility.get_transaction(
        transaction_id
    )


@router.get(
    "/wallet-transactions/claim-code/{claim_code}"
)
async def get_transactions_by_claim_code(
    claim_code: str
):
    return await (
        utility.get_transactions_by_claim_code(
            claim_code
        )
    )