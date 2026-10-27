from typing import Sequence
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Request, Depends
from webhook.utils import (
    load_webhook_signing_keys,
    webhook_validation,
    webhook_subscription)

from shared.core.constants import WEBHOOK_SUCCEEDED_RETURN, WebhookReturn
from shared.core.logging import setup_logger
from shared.core.config import get_db_session

setup_logger()
logger: logging.Logger = logging.getLogger(name=__name__)

app = FastAPI()

@app.post(path="/inventory_tracker_webhook")
async def store_inventory_data_webhook(
    request: Request,
    inventory_session:AsyncSession  = Depends(dependency=get_db_session))  -> WebhookReturn:

    if webhook_subscription(response=request):
        return WEBHOOK_SUCCEEDED_RETURN
    webhook_signing_keys: Sequence[str] | None = await load_webhook_signing_keys(session=inventory_session)
    await webhook_validation(request=request, webhook_signing_keys=webhook_signing_keys)
    return WEBHOOK_SUCCEEDED_RETURN
