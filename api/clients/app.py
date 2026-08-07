from fastapi import APIRouter, Depends

from core.security import verify_token

from api.clients.schema import (
    CreateClientSchema,
    UpdateClientSchema
)

from api.clients import utility

router = APIRouter()


@router.post("/clients")
async def create_client(
    data: CreateClientSchema,
    user=Depends(verify_token)
):
    return await utility.create_client(
        data.dict()
    )


@router.get("/clients")
async def get_clients():
    return await utility.get_clients()


@router.get("/clients/{client_id}")
async def get_client(
    client_id: str
):
    return await utility.get_client(
        client_id
    )


@router.put("/clients/{client_id}")
async def update_client(
    client_id: str,
    data: UpdateClientSchema,
    user=Depends(verify_token)
):
    payload = {
        k: v
        for k, v in data.dict().items()
        if v is not None
    }

    return await utility.update_client(
        client_id,
        payload
    )