from typing import TypedDict

class WebhookRequestTypeDict(TypedDict):
    headers: dict[str, str]
    body: dict[str, object]

mocked_webhook_subscription_event_valid: WebhookRequestTypeDict = {
    "headers": {
        "x-izettle-event-name": "TestMessage",
        "x-izettle-signature": "sha256=mocked_signature",
    },
    "body": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "transport_name": "WEBHOOK",
        "event_names": ["InventoryBalanceChanged"],
        "updated": "2024-06-01T12:00:00Z",
        "destination": "https://example.com/webhook",
        "contact_email": "test@example.com",
        "status": "ACTIVE",
        "signing_key": "test-signing-key",
    },
}

mocked_webhook_subscription_event_failed_status: WebhookRequestTypeDict = {
    "headers": {
        "x-izettle-event-name": "TestMessage",
        "x-izettle-signature": "sha256=mocked_signature",
    },
    "body": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "transport_name": "WEBHOOK",
        "event_names": ["InventoryBalanceChanged"],
        "updated": "2024-06-01T12:00:00Z",
        "destination": "https://example.com/webhook",
        "contact_email": "test@example.com",
        "status": "FAILED",
        "signing_key": "test-signing-key",
    },
}

mocked_webhook_subscription_event_invalid_data: WebhookRequestTypeDict = {
    "headers": {
        "x-izettle-event-name": "TestMessage",
        "x-izettle-signature": "sha256=mocked_signature",
    },
    "body": {
        "uuid": "not_uuid",
        "transport_name": "WEBHOOK",
        "event_names": ["InventoryBalanceChanged"],
        "updated": "2024-06-01T12:00:00Z",
        "destination": "https://example.com/webhook",
        "contact_email": "test@example.com",
        "status": "ACTIVE",
        "signing_key": "test-signing-key",
    },
}

mocked_webhook_subscription_event_missing_fields: WebhookRequestTypeDict = {
    "headers": {
        "x-izettle-event-name": "TestMessage",
        "x-izettle-signature": "sha256=mocked_signature",
    },
    "body": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "transport_name": "WEBHOOK",
        "event_names": ["InventoryBalanceChanged"],
        "updated": "2024-06-01T12:00:00Z",
        "status": "ACTIVE",
        "signing_key": "test-signing-key",
    },
}

mocked_webhook_subscription_event_invalid_uuid: WebhookRequestTypeDict = {
    "headers": {
        "x-izettle-event-name": "TestMessage",
        "x-izettle-signature": "sha256=mocked_signature",
    },
    "body": {
        "uuid": "invalid-uuid",
        "transport_name": "WEBHOOK",
        "event_names": ["InventoryBalanceChanged"],
        "updated": "2024-06-01T12:00:00Z",
        "destination": "https://example.com/webhook",
        "contact_email": "test@example.com",
        "status": "ACTIVE",
        "signing_key": "test-signing-key",
    },
}