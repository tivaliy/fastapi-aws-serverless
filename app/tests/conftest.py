from os import environ
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import create_application

# Set "test" settings environment
environ["APP_ENV"] = "test"


@pytest.fixture
def initialized_app():
    return create_application()


@pytest.fixture
def client(initialized_app) -> Generator:
    with TestClient(app=initialized_app) as c:
        yield c
