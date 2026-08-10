from fastapi import (
    APIRouter,
    UploadFile,
    File
)
import os

from api.claim_codes import utility

router = APIRouter()

os.makedirs("uploads/csv", exist_ok=True)

@router.post("/claim-codes/upload/{campaign_id}")
async def upload_claim_codes(
    campaign_id: str,
    file: UploadFile = File(...)
):
    upload_path = f"uploads/csv/{file.filename}"

    with open(upload_path, "wb") as buffer:
        buffer.write(await file.read())

    return await utility.upload_claim_codes(
        campaign_id,
        upload_path
    )


@router.get("/claim-codes")
async def get_claim_codes():
    return await utility.get_claim_codes()


@router.get("/claim-codes/{claim_code_id}")
async def get_claim_code(
    claim_code_id: str
):
    return await utility.get_claim_code(
        claim_code_id
    )


@router.get("/claim-codes/campaign/{campaign_id}")
async def get_claim_codes_by_campaign(
    campaign_id: str
):
    return await utility.get_claim_codes_by_campaign(
        campaign_id
    )