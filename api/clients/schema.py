from pydantic import BaseModel
from typing import Optional


class CreateClientSchema(BaseModel):
    client_name: str
    time_zone: str
    primary_contact: str
    active_status: bool = True


class UpdateClientSchema(BaseModel):
    client_name: Optional[str] = None
    time_zone: Optional[str] = None
    primary_contact: Optional[str] = None
    active_status: Optional[bool] = None