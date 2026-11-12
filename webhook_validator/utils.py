
import os
import hmac
import logging
import hashlib
from dataclasses import dataclass, field
from httpx import Request
from typing import  Union
from typing import Sequence,Union
from uuid import UUID 
from datetime import datetime
import pytz
import json

from pydantic import TypeAdapter
from shared.inventory_models import  InventoryBalanceUpdateValidator
from shared.constants import (
    UTC_TIMEZONE_NAME,
    SHOP_SUBSCRIPTION_EVENTS,
    WEBHOOK_NAME)
from .models import WebhookSubscriptionResponse 

logger: logging.Logger = logging.getLogger(name=__name__)


def webhook_subscription(response: Request) -> bool:
    if response.headers.get("x-izettle-event-name") == "TestMessage":
        return True
    return False


def webhook_validation(
    header: dict,
    body: dict,
    webhook_signing_keys: Sequence[str] | None
) -> None:
    received_signature: str | None = header.get("x-izettle-signature")
    if not webhook_signing_keys:
        raise PermissionError("No signing keys found for validation")
    if not received_signature:
        raise ValueError("Missing webhook signature")

    signature: str = received_signature.removeprefix("sha256=")
    raw_body: bytes = json.dumps(body).encode('utf-8')
    validated: bool = False
    for Key_data in webhook_signing_keys:
        expected_signature: str = hmac.new(
            key=Key_data.encode(encoding="utf-8"),
            msg=raw_body,
            digestmod=hashlib.sha256,
        ).hexdigest()
        if hmac.compare_digest(expected_signature, signature):
            validated = True
            break
    if not validated:
        raise PermissionError("Invalid webhook permission: signature mismatch")


def load_webhook_signing_keys() -> Sequence[str] | None:
    return None  #should be loaded from a secure storage or environment variable
    #should be loaded from a secure storage or environment variable

def if_idempotent() -> bool:
    # This function should check if the webhook has already been processed
    # For example, it could check a database or cache for a unique identifier in the webhook
    return False


logger: logging.Logger = logging.getLogger(name=__name__)


class ShopInfo:
    def __init__(self) -> None:
        self.dict = {
            UUID(os.environ["DALA_ORGANIZATION_UUID"]): "DALA_SHOP",
            UUID(os.environ["ART_ORGANIZATION_UUID"]): "ART_CRAFT",
            UUID(os.environ["CAFE_ORGANIZATION_UUID"]): "CAFE",
        }

    def get_shop_name_by_id(self, shop_id: UUID):
        return self.dict[shop_id]


def any_to_utc(date: datetime) -> datetime:
    """convert any timezone datetime to utc"""
    utc: datetime = date.astimezone(pytz.timezone(UTC_TIMEZONE_NAME))
    return utc


# @dataclass
# class CredentialContext:
#     shop_name: str
#     mail: str = os.environ["MAIL"]
#     events: list[str] = field(default_factory=list[str])
#     subscription_uuid: str = field(init=False)
#     destination_url: str = field(init=False)

#     def __post_init__(self):
#         self.subscription_uuid: str = os.environ[
#             f"{self.shop_name.upper()}_SUBSCRIPTION_UUID"
#         ]
#         self.destination_url: str = (
#             os.environ["DESTINATION_URL"] + "/" + WEBHOOK_NAME
#         )
#         self.events = SHOP_SUBSCRIPTION_EVENTS


AnyLambdaEvent = Union[WebhookSubscriptionResponse, InventoryBalanceUpdateValidator]
event_adapter: TypeAdapter[WebhookSubscriptionResponse | InventoryBalanceUpdateValidator] = TypeAdapter(AnyLambdaEvent)
