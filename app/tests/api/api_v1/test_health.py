from fastapi.testclient import TestClient
from starlette import status

from app.core.config import settings


def test_ping(client: TestClient) -> None:
    r = client.get(f"{settings.api_v1_prefix}/ping")
    assert r.json() == {"ping": "pong"}
    assert r.status_code == status.HTTP_200_OK
