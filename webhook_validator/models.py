from uuid import UUID
from typing import Literal
from datetime import datetime
from pydantic import BaseModel, HttpUrl, EmailStr

from shared.inventory_models import BaseSchema


class WebhookCheck(BaseModel):
    uuid: UUID
    status: str


class AccessToken(BaseModel):
    access_token: str
    expires_in: int


class WebhookSubscription(BaseSchema):
    uuid: UUID
    transport_name: Literal["WEBHOOK"]
    event_names: list[str]
    updated: datetime
    destination: HttpUrl
    contact_email: EmailStr
    status: str
    signing_key: str


class WebhookSubscriptionResponse(BaseSchema):
    uuid: UUID
    transport_name: Literal["WEBHOOK"]
    event_names: list[str]
    updated: datetime
    destination: HttpUrl
    contact_email: EmailStr
    status: str
