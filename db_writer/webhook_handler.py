import logging

from sqlalchemy.ext.asyncio import AsyncSession
from shared.core.inventory_models import InventoryBalanceUpdateValidator
from shared.core.repository import InventoryBalanceUpdateRepository
from db_writer.services import InventoryDBUpdater

logger: logging.Logger = logging.getLogger(name=__name__)


class SubscriptionHandler:
    async def process_subscription(
        self,
        inventory_update: InventoryBalanceUpdateValidator,
        session: AsyncSession,
    ) :

        logger.info(
            "Balance data: before=%i items, after=%d items",
            len(inventory_update.payload.balance_before),
            len(inventory_update.payload.balance_after),
            )

        inventory_update_repository: InventoryBalanceUpdateRepository = (
            InventoryBalanceUpdateRepository(session=session)
        )

        inventory_balance_updater = InventoryDBUpdater(
            inventory_balance_update=inventory_update,
            inventory_update_repository=inventory_update_repository,
        )

        return await inventory_balance_updater.store_inventory_update()