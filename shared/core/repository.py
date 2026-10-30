from dataclasses import dataclass
import logging
from typing import Sequence
from sqlalchemy import select
from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from shared.core.db_models import InventoryBalanceUpdateModel, PaypalPosSigningKey

logger: logging.Logger = logging.getLogger(name=__name__)


@dataclass
class InventoryBalanceUpdateRepository:
    session: AsyncSession

    async def store_inventory_data(
        self, inventory_update: InventoryBalanceUpdateModel
    )  -> None:
        self.session.add(instance=inventory_update)
        await self.session.commit()

class SigningKeyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_signing_keys(self) -> Sequence[str]:
        statement: SelectOfScalar = select(PaypalPosSigningKey.signing_key)
        results: Sequence[str] = (
            (await self.session.execute(statement=statement)).scalars().all()
        )
        return results