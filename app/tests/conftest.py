from os import environ

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import create_application

# Set "test" settings environment
environ["APP_ENV"] = "test"


@pytest.fixture
def initialized_app():
    return create_application()


@pytest.fixture
def client(initialized_app) -> TestClient:
    with TestClient(app=initialized_app) as c:
        yield c


@pytest.fixture
def authorized_client(client: TestClient, token: str) -> TestClient:
    client.headers = {
        "Authorization": f"{settings.jwt_token_prefix} {token}",
        **client.headers,
    }
    return client
