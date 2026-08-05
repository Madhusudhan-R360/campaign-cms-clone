from fastapi import APIRouter

from api.campaigns import utility

from api.campaigns.schema import (
    CreateCampaignSchema,
    UpdateCampaignSchema,
    CampaignProductSchema
)

router = APIRouter()

@router.post("/campaigns")
async def create_campaign(
    data: CreateCampaignSchema
):
    return await utility.create_campaign(
        data.model_dump()
    )


@router.get("/campaigns")
async def get_campaigns():
    return await utility.get_campaigns()


@router.get("/campaigns/{campaign_id}")
async def get_campaign(
    campaign_id: str
):
    return await utility.get_campaign(
        campaign_id
    )


@router.put("/campaigns/{campaign_id}")
async def update_campaign(
    campaign_id: str,
    data: UpdateCampaignSchema
):
    payload = {
        k: v
        for k, v in data.model_dump().items()
        if v is not None
    }

    return await utility.update_campaign(
        campaign_id,
        payload
    )

@router.post(
    "/campaigns/{campaign_id}/products"
)
async def add_product_to_campaign(
    campaign_id: str,
    data: CampaignProductSchema
):
    return await (
        utility.add_product_to_campaign(
            campaign_id,
            data.model_dump()
        )
    )


@router.get(
    "/campaigns/{campaign_id}/products"
)
async def get_campaign_products(
    campaign_id: str
):
    return await (
        utility.get_campaign_products(
            campaign_id
        )
    )