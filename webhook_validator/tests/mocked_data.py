from typing import TypedDict


class WebhookSubscriptionTypeDict(TypedDict):
    headers: dict[str, str]
    body: dict[str, object]


mocked_webhook_subscription_event_valid: WebhookSubscriptionTypeDict = {
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

mocked_webhook_subscription_event_failed_status: WebhookSubscriptionTypeDict = {
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

mocked_webhook_subscription_event_invalid_data: WebhookSubscriptionTypeDict = {
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

mocked_webhook_subscription_event_missing_fields: WebhookSubscriptionTypeDict = {
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

mocked_webhook_subscription_event_invalid_uuid: WebhookSubscriptionTypeDict = {
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


mocked_webhook_subscription_event_invalid_uuid: WebhookSubscriptionTypeDict = {
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

mocked_inventory_body_valid = {
    "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
    "messageUuid": "223e4567-e89b-12d3-a456-426614174000",
    "eventName": "InventoryBalanceChanged",
    "messageId": "323e4567-e89b-12d3-a456-426614174000",
    "payload": {
        "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
        "updated": {
            "uuid": "423e4567-e89b-12d3-a456-426614174000",
            "timestamp": "2026-11-27T11:30:00Z",
            "userType": "USER",
            "clientUuid": None,
        },
        "balanceBefore": [
            {
                "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
                "locationUuid": "523e4567-e89b-12d3-a456-426614174000",
                "productUuid": "623e4567-e89b-12d3-a456-426614174000",
                "variantUuid": "723e4567-e89b-12d3-a456-426614174000",
                "balance": 10,
            }
        ],
        "balanceAfter": [
            {
                "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
                "locationUuid": "523e4567-e89b-12d3-a456-426614174000",
                "productUuid": "623e4567-e89b-12d3-a456-426614174000",
                "variantUuid": "723e4567-e89b-12d3-a456-426614174000",
                "balance": 8,
            }
        ],
        "externalUuid": None,
    },
    "timestamp": "2026-11-27T11:30:01Z",
}

mocked_inventory_body_invalid_uuid = {
    "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
    "messageUuid": "223e4567-e89b-12d3-a456-",
    "eventName": "InventoryBalanceChanged",
    "messageId": "323e4567-e89b-12d3-a456-426614174000",
    "payload": {
        "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
        "updated": {
            "uuid": "423e4567-e89b-12d3-a456-426614174000",
            "timestamp": "2026-11-27T11:30:00Z",
            "userType": "USER",
            "clientUuid": None,
        },
        "balanceBefore": [
            {
                "organizationUuid": "123e4567-e89b-12d3-a456-",
                "locationUuid": "523e4567-e89b-12d3-a456-426614174000",
                "productUuid": "623e4567-e89b-12d3-a456-426614174000",
                "variantUuid": "723e4567-e89b-12d3-a456-426614174000",
                "balance": 10,
            }
        ],
        "balanceAfter": [
            {
                "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
                "locationUuid": "523e4567-e89b-12d3-a456-426614174000",
                "productUuid": "623e4567-e89b-12d3-a456-426614174000",
                "variantUuid": "723e4567-e89b-12d3-a456-426614174000",
                "balance": 8,
            }
        ],
        "externalUuid": None,
    },
    "timestamp": "2026-11-27T11:30:01Z",
}


mocked_inventory_body_empty_field = {
    "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
    "messageUuid": "223e4567-e89b-12d3-a456-426614174000",
    "eventName": "InventoryBalanceChanged",
    "messageId": "323e4567-e89b-12d3-a456-426614174000",
    "payload": {
        "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
        "updated": {
            "uuid": "423e4567-e89b-12d3-a456-426614174000",
            "timestamp": "2026-11-27T11:30:00Z",
            "userType": "USER",
            "clientUuid": None,
        },
        "balanceBefore": [
            {
                "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
                "locationUuid": "523e4567-e89b-12d3-a456-426614174000",
                "productUuid": "623e4567-e89b-12d3-a456-426614174000",
                "variantUuid": "723e4567-e89b-12d3-a456-426614174000",
                "balance": "",  # invalid_field
            }
        ],
        "balanceAfter": [
            {
                "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
                "locationUuid": "523e4567-e89b-12d3-a456-426614174000",
                "productUuid": "623e4567-e89b-12d3-a456-426614174000",
                "variantUuid": "723e4567-e89b-12d3-a456-426614174000",
                "balance": 8,
            }
        ],
        "externalUuid": None,
    },
    "timestamp": "2026-11-27T11:30:01Z",
}

mocked_inventory_body_empty_balance_after = {
    "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
    "messageUuid": "223e4567-e89b-12d3-a456-426614174000",
    "eventName": "InventoryBalanceChanged",
    "messageId": "323e4567-e89b-12d3-a456-426614174000",
    "payload": {
        "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
        "updated": {
            "uuid": "423e4567-e89b-12d3-a456-426614174000",
            "timestamp": "2026-11-27T11:30:00Z",
            "userType": "USER",
            "clientUuid": None,
        },
        "balanceBefore": [
            {
                "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
                "locationUuid": "523e4567-e89b-12d3-a456-426614174000",
                "productUuid": "623e4567-e89b-12d3-a456-426614174000",
                "variantUuid": "723e4567-e89b-12d3-a456-426614174000",
                "balance": 10,
            }
        ],
        "balanceAfter": [
            {
                # empty balance after
            }
        ],
        "externalUuid": None,
    },
    "timestamp": "2026-11-27T11:30:01Z",
}

mocked_inventory_body_empty_payload = {
    "organizationUuid": "123e4567-e89b-12d3-a456-426614174000",
    "messageUuid": "223e4567-e89b-12d3-a456-426614174000",
    "eventName": "InventoryBalanceChanged",
    "messageId": "323e4567-e89b-12d3-a456-426614174000",
    "payload": {
        # empty payload
    },
    "timestamp": "2026-11-27T11:30:01Z",
}
