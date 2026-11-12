import pytest
from copy import deepcopy
from pydantic import ValidationError
import json
from webhook_validator.tests.mocked_data import (
    mocked_webhook_subscription_event_valid,
    mocked_webhook_subscription_event_failed_status,
    mocked_webhook_subscription_event_invalid_data,
    mocked_webhook_subscription_event_missing_fields,
    mocked_webhook_subscription_event_invalid_uuid
)
from webhook_validator.type_dict import WebhookRequestTypeDict
from webhook_validator.webhook_request_validator import webhook_handler
import hmac
import hashlib
from webhook_validator.utils import webhook_validation

def test_webhook_subscription_active_status():

    result: None | dict = webhook_handler(mocked_webhook_subscription_event_valid, None)
    assert result is not None
    assert result.get("statusCode") == 200
    assert result.get("body") == "Webhook subscription event received successfully"

@pytest.mark.parametrize(
    argnames="mocked_event",
    argvalues=[
        mocked_webhook_subscription_event_invalid_data,
        mocked_webhook_subscription_event_missing_fields,
        mocked_webhook_subscription_event_invalid_uuid

    ]
)
def test_webhook_subscription_invalid_request_body(mocked_event):
    with pytest.raises(ValidationError):
        webhook_handler(mocked_event, None)

@pytest.mark.parametrize(
    argnames="mocked_event",
    argvalues=[
        mocked_webhook_subscription_event_failed_status
    ]
)
def test_webhook_subscription_failed_status(mocked_event):
    with pytest.raises(expected_exception=ValueError, match="Webhook subscription is not active"):
        webhook_handler(mocked_event, None)

def test_webhook_validation_with_valid_signature():
    mocked_event = deepcopy(mocked_webhook_subscription_event_valid)
    body: dict[str, object] =  mocked_event.get("body")
    valid_key: str = "valid_key_1"
    raw_body: bytes = json.dumps(body).encode('utf-8')
    
    valid_signature: str = hmac.new(
            key=valid_key.encode(encoding="utf-8"),
            msg=raw_body,
            digestmod=hashlib.sha256,
        ).hexdigest()

    mocked_event["headers"]["x-izettle-signature"] = f"sha256={valid_signature}"
    webhook_signing_keys: list[str] = [valid_key, "invalid_key_2", "invalid_key_3"]

    result: None = webhook_validation(
        header=mocked_event.get("headers"),
        body=mocked_event.get("body"),
        webhook_signing_keys=webhook_signing_keys)

    assert result is None  # If no exception is raised, the validation passed


def test_webhook_validation_with_invalid_signature():
    mocked_event = deepcopy(mocked_webhook_subscription_event_valid)
    body: dict[str, object] =  mocked_event.get("body")
    valid_key: str = "valid_key_1"
    raw_body: bytes = json.dumps(body).encode('utf-8')
    
    valid_signature: str = hmac.new(
            key=valid_key.encode(encoding="utf-8"),
            msg=raw_body,
            digestmod=hashlib.sha256,
        ).hexdigest()

    mocked_event["headers"]["x-izettle-signature"] = f"sha256={valid_signature}"
    webhook_signing_keys: list[str] = ['invalid_key_1', "invalid_key_2", "invalid_key_3"]
    with pytest.raises(expected_exception=PermissionError, match="Invalid webhook permission: signature mismatch"):
        webhook_validation(
            header=mocked_event.get("headers"),
            body=mocked_event.get("body"),
            webhook_signing_keys=webhook_signing_keys)


def test_idempotent_behavior():
    mocked_event = deepcopy(mocked_webhook_subscription_event_valid)
    with pytest.raises(expected_exception=ValueError, match="Duplicate webhook received"):
        webhook_handler(mocked_event, None)