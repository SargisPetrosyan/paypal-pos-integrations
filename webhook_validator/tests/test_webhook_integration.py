# from unittest.mock import patch

# import pytest

# from shared.inventory_models import InventoryBalanceUpdateValidator

# from .mocked_data import (
#     mocked_webhook_subscription_event_failed_status,
#     mocked_webhook_subscription_event_valid,
# )


# def test_valid_subscription(
#     lambda_module, mock_dsql_connector
# ):
#     with patch.object(mock_dsql_connector, "store_signing_keys") as store_signing_keys:
#         response = lambda_module.lambda_handler(
#             mocked_webhook_subscription_event_valid, None
#         )

#     assert response == {
#         "statusCode": 200,
#         "body": "Webhook subscription event received successfully",
#     }
#     store_signing_keys.assert_called_once()
#     assert store_signing_keys.call_args.kwargs["subscription"].signing_key == (
#         "test-signing-key"
#     )
#     mock_dsql_connector.get_signing_keys.assert_not_called()


# def test_inventory_event_uses_mocked_signing_keys(lambda_module, mock_dsql_connector):
#     event: InventoryBalanceUpdateValidator = InventoryBalanceUpdateValidator.model_construct()
#     body = {"event": "inventory update"}
#     headers = {"x-izettle-signature": "sha256=test"}
#     signing_keys = [("test-signing-key",)]

#     with (
#         patch.object(
#             lambda_module.event_adapter, "validate_python", return_value=event
#         ),
#         patch.object(
#             mock_dsql_connector, "get_signing_keys", return_value=signing_keys
#         ) as get_signing_keys,
#         patch.object(lambda_module, "webhook_validation") as webhook_validation,
#     ):
#         lambda_module.lambda_handler({"headers": headers, "body": body}, None)

#     get_signing_keys.assert_called_once_with()
#     webhook_validation.assert_called_once_with(
#         header=headers, body=body, webhook_signing_keys=signing_keys
#     )


# def test_inactive_subscription_does_not_store_signing_key(
#     lambda_module, mock_dsql_connector
# ):
#     with (
#         patch.object(mock_dsql_connector, "store_signing_keys") as store_signing_keys,
#         patch.object(mock_dsql_connector, "get_signing_keys") as get_signing_keys,
#         pytest.raises(ValueError, match="Webhook subscription is not active"),
#     ):
#         lambda_module.lambda_handler(
#             mocked_webhook_subscription_event_failed_status, None
#         )

#     store_signing_keys.assert_not_called()
#     get_signing_keys.assert_not_called()
