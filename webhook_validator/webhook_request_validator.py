from typing import Sequence
from shared.inventory_models import InventoryBalanceUpdateValidator
from .utils import (
    WebhookSubscriptionResponse,
    if_idempotent,
    load_webhook_signing_keys,
    webhook_validation)
from .utils import event_adapter
from .type_dict import WebhookRequestTypeDict


def webhook_handler(_event: WebhookRequestTypeDict, _context) -> None | dict:
    header: dict = _event.get("headers")
    body:dict = _event.get("body")
    event: WebhookSubscriptionResponse | InventoryBalanceUpdateValidator = event_adapter.validate_python(body)
    if isinstance(event, WebhookSubscriptionResponse):
        if event.status != "ACTIVE":
            raise ValueError("Webhook subscription is not active")
        return {"statusCode": 200, "body": "Webhook subscription event received successfully"}
    webhook_signing_keys: Sequence[str] | None = load_webhook_signing_keys()
    webhook_validation(header=header, body=body, webhook_signing_keys=webhook_signing_keys)
    if if_idempotent():
        raise ValueError("Duplicate webhook received")
    # put in a SQS queue for processing
