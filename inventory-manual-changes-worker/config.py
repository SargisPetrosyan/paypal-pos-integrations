import os
from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlmodel import create_engine
import aurora_dsql_psycopg as dsql
from shared.constants import AURORA_DSQL_USER
load_dotenv()

DSQL_DB_CLUSTER = os.getenv('DSQL_DB_CLUSTER')
AURORA_DSQL_USER = os.getenv('AURORA_DSQL_USER')

class DatabaseConnection:
    @staticmethod
    def create_engine() -> Engine:
        return create_engine(
            "postgresql+psycopg://",
            creator=lambda: dsql.connect(host=DSQL_DB_CLUSTER, user=AURORA_DSQL_USER, autocommit=True),
            isolation_level="AUTOCOMMIT",
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=0,
            pool_recycle=3300,  # Recycle before DSQL's 1-hour limit
        )