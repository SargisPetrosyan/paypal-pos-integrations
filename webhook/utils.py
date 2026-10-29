import os
import hmac
import logging
import hashlib
from typing import Sequence
from uuid import UUID
from datetime import datetime
import pytz
from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, select
from sqlmodel.sql._expression_select_cls import SelectOfScalar
from fastapi import HTTPException, Request
from shared.core.db_models import PaypalMessageIdLog, PaypalPosSigningKey
from shared.core.inventory_models import InventoryBalanceUpdateValidator
from shared.core.constants import (
    UTC_TIMEZONE_NAME,
    SHOP_SUBSCRIPTION_EVENTS,
    WEBHOOK_NAME)

logger: logging.Logger = logging.getLogger(name=__name__)


def webhook_subscription(response: Request) -> bool:
    if response.headers.get("x-izettle-event-name") == "TestMessage":
        return True
    return False


async def webhook_validation(
    request: Request, webhook_signing_keys: Sequence[str] | None
) -> None:
    if not webhook_signing_keys:
        raise HTTPException(
            status_code=401, detail="No signing keys found for validation"
        )

    received_signature: str = request.headers.get("x-izettle-signature", "")
    if received_signature == "":
        raise HTTPException(status_code=401, detail="Missing webhook signature")

    raw_body: bytes = await request.body()
    validated: bool = False
    for Key_data in webhook_signing_keys:
        expected_signature: str = hmac.new(
            key=Key_data.encode(encoding="utf-8"),
            msg=raw_body,
            digestmod=hashlib.sha256,
        ).hexdigest()
        if received_signature.startswith("sha256="):
            received_signature = received_signature.split("sha256=")[1]
        if hmac.compare_digest(expected_signature, received_signature):
            validated = True
            break
    if not validated:
        raise HTTPException(status_code=401, detail="Invalid webhook signature")


async def load_webhook_signing_keys(session: AsyncSession) -> Sequence[str] | None:
    statement: SelectOfScalar = select(PaypalPosSigningKey.signing_key)
    results: Sequence[str] = (
        (await session.execute(statement=statement)).scalars().all()
    )
    return results


class SigningKeyEngine:
    def __init__(self) -> None:
        self.engine: Engine = create_engine(os.environ["SIGNING_KEYS_DB_URL"])
        SQLModel.metadata.create_all(self.engine)


async def check_idempotency(
    validated_request_body: InventoryBalanceUpdateValidator, session: AsyncSession
) -> bool:
    statement: SelectOfScalar = select(PaypalMessageIdLog.message_id).where(
        PaypalMessageIdLog.message_id == validated_request_body.message_id
    )
    result: Sequence[str] = (await session.execute(statement=statement)).scalars().all()
    if result:
        return True
    return False


logger: logging.Logger = logging.getLogger(name=__name__)


class ShopInfo:
    def __init__(self) -> None:
        self.dict = {
            UUID(os.environ["DALA_ORGANIZATION_UUID"]): "DALA_SHOP",
            UUID(os.environ["ART_ORGANIZATION_UUID"]): "ART_CRAFT",
            UUID(os.environ["CAFE_ORGANIZATION_UUID"]): "CAFE",
        }

    def get_shop_name_by_id(self, shop_id: UUID):
        return self.dict[shop_id]


def any_to_utc(date: datetime) -> datetime:
    """convert any timezone datetime to utc"""
    utc: datetime = date.astimezone(pytz.timezone(UTC_TIMEZONE_NAME))
    return utc


@dataclass
class CredentialContext:
    shop_name: str
    mail: str = os.environ["MAIL"]
    events: list[str] = field(default_factory=list[str])
    subscription_uuid: str = field(init=False)
    destination_url: str = field(init=False)

    def __post_init__(self):
        self.subscription_uuid: str = os.environ[
            f"{self.shop_name.upper()}_SUBSCRIPTION_UUID"
        ]
        self.destination_url: str = (
            os.environ["DESTINATION_URL"] + "/" + WEBHOOK_NAME
        )
        self.events = SHOP_SUBSCRIPTION_EVENTS
