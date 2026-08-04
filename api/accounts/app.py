from fastapi import APIRouter

from api.accounts.schema import (
    CreateAccountSchema,
    UpdateAccountSchema
)

from api.accounts import utility

router = APIRouter()

@router.post("/accounts")
async def create_account(
    data: CreateAccountSchema
):
    return await utility.create_account(
        data.dict()
    )

@router.get("/accounts")
async def get_accounts():
    return await utility.get_accounts()

@router.get(
    "/accounts/{account_id}"
)
async def get_account(
    account_id: str
):
    return await utility.get_account(
        account_id
    )

@router.get(
    "/accounts/client/{client_id}"
)
async def get_accounts_by_client(
    client_id: str
):
    return await utility.get_accounts_by_client(
        client_id
    )

@router.put(
    "/accounts/{account_id}"
)
async def update_account(
    account_id: str,
    data: UpdateAccountSchema
):

    payload = {
        k: v
        for k, v in data.dict().items()
        if v is not None
    }

    return await utility.update_account(
        account_id,
        payload
    )