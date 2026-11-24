import os
from typing import Sequence

# pylint:disable=import-error
from dotenv import load_dotenv
import aurora_dsql_psycopg as dsql
from shared.constants import INVENTORY_DB_TABLE_NAME, SIGNING_KEY_TABLE_NAME
from models import WebhookSubscription

load_dotenv()


class DSQLConnector:
    def __init__(self) -> None:
        self.inventory_table_name: str = INVENTORY_DB_TABLE_NAME
        self.signing_keys_table_name: str = SIGNING_KEY_TABLE_NAME
        DSQL_CLUSTER: str = os.environ["DSQL_DB_CLUSTER"]
        DSQL_ZONE: str = os.environ["DSQL_ZONE"]
        USER: str = os.environ["DSQL_USER"]
        self.config = {
            "host": DSQL_CLUSTER + ".dsql." + DSQL_ZONE + ".on.aws",
            "region": DSQL_ZONE,
            "user": USER,
        }
        self.conn = dsql.connect(**self.config)  # type: ignore

    def get_all_inventory_items(self):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.inventory_table_name}")
            return cur.fetchall()

    def store_inventory_item(self, values: Sequence[str]) -> None:
        placeholders: str = ", ".join(["%s"] * len(values))

        with self.conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {self.inventory_table_name} VALUES ({placeholders});"
            )
            self.conn.commit()

    def store_inventory_items(self, values: Sequence[Sequence[str]]):
        placeholders: str = ", ".join(["%s"] * len(values[0]))

        with self.conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {self.inventory_table_name} VALUES ({placeholders});"
            )
            self.conn.commit()

    def get_signing_keys(self) -> list[tuple[str]]:
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.signing_keys_table_name};")
            return cur.fetchall()

    def store_signing_keys(self, subscription: WebhookSubscription) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT COUNT(*) FROM {self.signing_keys_table_name} WHERE shop_id = {str(subscription.uuid)};"
            )

            if cur.fetchone()[0] > 0:
                cur.execute(f"""
                UPDATE items SET 
                shop_id = '{subscription.uuid}',
                signing_key = '{subscription.signing_key}',
                updated = '{subscription.updated}' 
                WHERE uuid = '{str(subscription.uuid)}';""")

            else:
                cur.execute(f"""
                INSERT INTO {self.signing_keys_table_name} 
                VALUES ('{str(subscription.uuid)}','{subscription.signing_key}','{subscription.updated}');""")
