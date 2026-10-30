from typing import Sequence
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Request, Depends
import uvicorn
from shared.core.inventory_models import InventoryBalanceUpdateValidator
from webhook.utils import (
    check_idempotency,
    load_webhook_signing_keys,
    webhook_validation)
from webhook.webhook_handler import WebhookHandler
from webhook.models.webhook import WebhookSubscriptionResponse

from shared.core.logging import setup_logger
from shared.core.config import get_db_session

# setup_logger()
logger: logging.Logger = logging.getLogger(name=__name__)
webhook_handler: WebhookHandler = WebhookHandler()

app = FastAPI()


@app.post(path="/inventory_tracker_webhook")
async def store_inventory_data_webhook(
    http_request: Request,
    request: WebhookSubscriptionResponse | InventoryBalanceUpdateValidator,
    inventory_session: AsyncSession = Depends(dependency=get_db_session),
) -> None:

    if isinstance(request, WebhookSubscriptionResponse):
        return
    webhook_signing_keys: Sequence[str] | None = await load_webhook_signing_keys(session=inventory_session)
    await webhook_validation(request=http_request, webhook_signing_keys=webhook_signing_keys)
    if await check_idempotency(request=request, session=inventory_session):
        raise ValueError(
            "Duplicate webhook received. This webhook has already been processed."
        )
    await webhook_handler.process_webhook(inventory_update=request, session=inventory_session)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
