import uuid
import datetime
from sqlmodel import Field, SQLModel, DateTime


class InventoryBalanceUpdateModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime.datetime = Field(default_factory=DateTime)
    organization_uuid: uuid.UUID = Field(default_factory=uuid.uuid4)
    product_uuid: uuid.UUID = Field(default_factory=uuid.uuid1)
    variant_uuid: uuid.UUID = Field(default_factory=uuid.uuid1)
    before: int
    after: int

    def __repr__(self) -> str:
        return f"""<InventoryBalanceUpdate(
        timestamp='{self.timestamp},
        before:{self.before},
        after:{self.after},
        change:{self.after}')>"""
        
class PaypalPosSigningKey(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    shop_id: uuid.UUID = Field(default_factory=uuid.uuid1, index=True)
    signing_key: str
    updated: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)

    def __repr__(self) -> str:
        return f"""<PaypalPosSigningKey(
        shop_id:{self.shop_id},
        signing_key:{self.signing_key},
        updated:{self.updated})>"""
        
class PaypalMessageIdLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    message_id: uuid.UUID = Field(unique=True, index=True)