from dotenv import load_dotenv
from shared.inventory_models import InventoryBalanceUpdateValidator

# pylint:disable=import-error
from db_connect import DSQLConnector
from models import WebhookSubscription

from utils import webhook_validation, event_adapter  # type: ignore

load_dotenv()
dsql_connector = DSQLConnector()


def lambda_handler(event, contex):  # type: ignore
    header: dict = event.get("headers")
    body: dict = event.get("body")
    event: WebhookSubscription | InventoryBalanceUpdateValidator = (
        event_adapter.validate_python(body)
    )
    if isinstance(event, WebhookSubscription):
        if event.status != "ACTIVE":
            raise ValueError("Webhook subscription is not active")
        dsql_connector.store_signing_keys(subscription=event)
        return {
            "statusCode": 200,
            "body": "Webhook subscription event received successfully",
        }
    webhook_signing_keys: list[tuple[str]] = dsql_connector.get_signing_keys()
    webhook_validation(
        header=header, body=body, webhook_signing_keys=webhook_signing_keys
    )
