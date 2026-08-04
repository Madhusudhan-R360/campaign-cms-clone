from pydantic import BaseModel
from typing import Optional


class CreateAccountSchema(BaseModel):
    account_name: str
    description: str
    client_id: str
    active_status: bool = True


class UpdateAccountSchema(BaseModel):
    account_name: Optional[str] = None
    description: Optional[str] = None
    active_status: Optional[bool] = None