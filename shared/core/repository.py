from dataclasses import dataclass
import logging
from shared.core.constants import WEBHOOK_SUCCEEDED_RETURN, WebhookReturn
from sqlalchemy.ext.asyncio import AsyncSession
from shared.core.db_models import InventoryBalanceUpdateModel

logger: logging.Logger = logging.getLogger(name=__name__)


@dataclass
class InventoryBalanceUpdateRepository:
    session: AsyncSession

    async def store_inventory_data(
        self, inventory_update: InventoryBalanceUpdateModel
    ) -> WebhookReturn:

        try:
            self.session.add(instance=inventory_update)
            await self.session.commit()
            return WEBHOOK_SUCCEEDED_RETURN
        except Exception as e:
            await self.session.rollback()
            raise e