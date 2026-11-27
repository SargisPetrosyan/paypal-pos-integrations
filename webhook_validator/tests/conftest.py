import importlib
import sys
from types import ModuleType
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(scope="module")
def lambda_module():
    connector = MagicMock()
    mocked_db_connect = ModuleType("db_connect")
    mocked_db_connect.__dict__["DSQLConnector"] = MagicMock(return_value=connector)
    models_module: ModuleType = importlib.import_module("models")

    with patch.dict(
        sys.modules,
        {"db_connect": mocked_db_connect, "models": models_module},
    ):
        utils_module: ModuleType = importlib.import_module("webhook_validator.utils")
        with patch.dict(sys.modules, {"utils": utils_module}):
            yield importlib.import_module("webhook_validator.lambda_function")


@pytest.fixture
def mock_dsql_connector(lambda_module: ModuleType):
    connector = lambda_module.dsql_connector
    connector.reset_mock()
    return connector
