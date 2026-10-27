from dataclasses import dataclass
import logging
from shared.core.constants import WebhookReturn
from shared.core.db_models import InventoryBalanceUpdateModel
from shared.core.inventory_models import InventoryBalanceUpdateValidator
from shared.core.repository import InventoryBalanceUpdateRepository

logger: logging.Logger = logging.getLogger(name=__name__)


@dataclass
class InventoryDBUpdater:
    inventory_balance_update: InventoryBalanceUpdateValidator
    inventory_update_repository: InventoryBalanceUpdateRepository

    async def store_inventory_update(self) -> WebhookReturn:
        inventory_update:InventoryBalanceUpdateModel = InventoryBalanceUpdateModel(
            timestamp=self.inventory_balance_update.timestamp,
            organization_uuid=self.inventory_balance_update.payload.organization_uuid,
            product_uuid=self.inventory_balance_update.payload.balance_before[0].product_uuid,
            variant_uuid=self.inventory_balance_update.payload.balance_before[0].variant_uuid,
            before=self.inventory_balance_update.payload.balance_before[0].balance,
            after=self.inventory_balance_update.payload.balance_after[0].balance
            )

        return await self.inventory_update_repository.store_inventory_data(
            inventory_update=inventory_update
        )
