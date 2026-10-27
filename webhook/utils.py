import os
import hmac
import logging
import hashlib
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, select
from sqlmodel.sql._expression_select_cls import SelectOfScalar
from fastapi import HTTPException, Request
from shared.core.db_models import PaypalMessageIdLog, PaypalPosSigningKey

logger: logging.Logger = logging.getLogger(name=__name__)


def webhook_subscription(response: Request) -> bool:
    if response.headers.get("x-izettle-event-name") == "TestMessage":
        return True
    return False


async def webhook_validation(request:Request, webhook_signing_keys:Sequence[str] | None) -> None:
    if not webhook_signing_keys:
        raise HTTPException(
            status_code=401,
            detail="No signing keys found for validation"
        )
    received_signature: str = request.headers.get("x-izettle-signature", "")
    raw_body: bytes = await request.body()
    validated:bool = False
    for Key_data in webhook_signing_keys:
        expected_signature: str = hmac.new(
            key=Key_data.encode(encoding="utf-8"),
            msg=raw_body,
            digestmod=hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(expected_signature, received_signature):
            validated = True
            break
    if not validated:
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature"
        )

    
async def load_webhook_signing_keys(session: AsyncSession) -> Sequence[str] | None:
    statement: SelectOfScalar = select(PaypalPosSigningKey.signing_key)
    results: Sequence[str] = (await session.execute(statement=statement)).scalars().all()
    return results


class SigningKeyEngine():
    def __init__(self)  -> None:
        self.engine: Engine = create_engine(os.environ["SIGNING_KEYS_DB_URL"])
        SQLModel.metadata.create_all(self.engine)

async def check_idempotency_key(request:Request, session: AsyncSession) -> bool:
    request_data = await request.json()
    statement: SelectOfScalar = select(PaypalMessageIdLog.message_id).where(
        PaypalMessageIdLog.message_id == request_data.get("message_id")
    )
    result: Sequence[str] = (await session.execute(statement=statement)).scalars().all()
    if result:
        return True
    return False