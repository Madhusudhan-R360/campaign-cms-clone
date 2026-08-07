from fastapi import APIRouter

from api.auth import utility

from api.auth.schema import (
    RegisterSchema,
    LoginSchema
)

router = APIRouter()

@router.post("/auth/register")
async def register_user(
    data: RegisterSchema
):
    return await utility.register_user(
        data.model_dump()
    )

@router.post("/auth/login")
async def login_user(
    data: LoginSchema
):
    return await utility.login_user(
        data.model_dump()
    )