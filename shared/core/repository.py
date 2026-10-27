from dataclasses import dataclass
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from shared.core.db_models import InventoryBalanceUpdateModel

logger: logging.Logger = logging.getLogger(name=__name__)


@dataclass
class InventoryBalanceUpdateRepository:
    session: AsyncSession

    async def store_inventory_data(
        self, inventory_update: InventoryBalanceUpdateModel
    ) -> dict:

        try:
            self.session.add(instance=inventory_update)
            await self.session.commit()
            return {"message": "Data registered in db"}
        except Exception as e:
            await self.session.rollback()
            raise e