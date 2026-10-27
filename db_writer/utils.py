import os
import logging
from uuid import UUID

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