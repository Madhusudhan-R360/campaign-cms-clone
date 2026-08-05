from pydantic import BaseModel


class ClaimCodeUploadSchema(BaseModel):
    campaign_id: str