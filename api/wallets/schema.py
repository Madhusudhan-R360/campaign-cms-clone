from pydantic import BaseModel


class GenerateWalletSchema(BaseModel):
    campaign_id: str