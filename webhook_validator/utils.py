import hmac
import json
import logging
import hashlib
from typing import Union
# pylint:disable=import-error

from pydantic import TypeAdapter
from shared.inventory_models import InventoryBalanceUpdateValidator

from models import WebhookSubscription

logger: logging.Logger = logging.getLogger(name=__name__)


def webhook_validation(
    header: dict, body: dict, webhook_signing_keys: list[tuple[str]] | None
) -> None:
    received_signature: str | None = header.get("x-izettle-signature")
    if not webhook_signing_keys:
        raise PermissionError("No signing keys found for validation")
    if not received_signature:
        raise ValueError("Missing webhook signature")

    signature: str = received_signature.removeprefix("sha256=")
    raw_body: bytes = json.dumps(body).encode("utf-8")
    validated: bool = False
    for Key_data in webhook_signing_keys[0]:
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


AnyLambdaEvent = Union[WebhookSubscription, InventoryBalanceUpdateValidator]
event_adapter: TypeAdapter[WebhookSubscription | InventoryBalanceUpdateValidator] = (
    TypeAdapter(AnyLambdaEvent)
)
