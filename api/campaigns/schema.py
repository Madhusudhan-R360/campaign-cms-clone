from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class CreateCampaignSchema(BaseModel):

    name: str

    account_id: str

    start_date: datetime

    end_date: datetime

    active_status: bool = True


class UpdateCampaignSchema(BaseModel):

    name: Optional[str] = None

    start_date: Optional[datetime] = None

    end_date: Optional[datetime] = None

    active_status: Optional[bool] = None


class CampaignProductSchema(BaseModel):

    product_id: str

    min_qty: int = 1

    max_qty: int = 10