# from unittest.mock import patch
# from pydantic import ValidationError

# import pytest

# from shared.inventory_models import InventoryBalanceUpdateValidator

# from .mocked_data import (
#     mocked_inventory_body_empty_balance_after,
#     mocked_inventory_body_empty_payload,
#     mocked_inventory_body_valid,
#     mocked_inventory_body_empty_field,
#     mocked_inventory_body_invalid_uuid
# )

# @pytest.mark.parametrize(
#     argnames="mocked_event",
#     argvalues=[
#         mocked_inventory_body_empty_payload,
#         mocked_inventory_body_empty_balance_after,
#         mocked_inventory_body_empty_field,
#         mocked_inventory_body_invalid_uuid
#     ],
# )

# def test_webhook_event_invalid_body(
#     mocked_event, lambda_module
# ):
#     with pytest.raises(expected_exception=ValidationError):
#         lambda_module.lambda_handler(mocked_event, None)


# def test_inventory_event_uses_mocked_signing_keys(lambda_module, mock_dsql_connector):
#     signing_keys = [("test-signing-key",)]
#     headers = {"x-izettle-signature": "sha256=test"}

#     with (
#         patch.object(
#             mock_dsql_connector, "get_signing_keys", return_value=signing_keys
#         ) as get_signing_keys, ):
#         lambda_module.lambda_handler({"headers": headers, "body": mocked_inventory_body_valid}, None)

#     get_signing_keys.assert_called_once_with()

