from typing import Sequence
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, HTTPException, Request, Depends
from shared.core.inventory_models import InventoryBalanceUpdateValidator
from webhook.utils import (
    check_idempotency,
    load_webhook_signing_keys,
    webhook_validation,
    webhook_subscription)
from webhook.webhook_handler import WebhookHandler

from shared.core.logging import setup_logger
from shared.core.constants import (
    WEBHOOK_SUCCEEDED_RETURN, 
    WebhookSuccessReturn)
from shared.core.config import get_db_session

setup_logger()
logger: logging.Logger = logging.getLogger(name=__name__)
webhook_handler: WebhookHandler = WebhookHandler()

app = FastAPI()

@app.post(path="/inventory_tracker_webhook")
async def store_inventory_data_webhook(
    request: Request,
    inventory_session:AsyncSession  = Depends(dependency=get_db_session))  -> WebhookSuccessReturn | HTTPException:

    if webhook_subscription(response=request):
        return WEBHOOK_SUCCEEDED_RETURN
    
    webhook_signing_keys: Sequence[str] | None = await load_webhook_signing_keys(session=inventory_session)
    await webhook_validation(request=request, webhook_signing_keys=webhook_signing_keys)
    validated_request_body: InventoryBalanceUpdateValidator = InventoryBalanceUpdateValidator.model_validate_json(json_data=await request.json())
    if await check_idempotency(validated_request_body=validated_request_body, session=inventory_session):
        return HTTPException(status_code=409, detail="Idempotency key already exists")
    return await webhook_handler.process_webhook(inventory_update=validated_request_body, session=inventory_session)
