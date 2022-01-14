from fastapi.testclient import TestClient
from starlette import status

from app.core.settings.app import AppSettings


def test_ping(client: TestClient, settings: AppSettings) -> None:
    r = client.get(f"{settings.api_v1_prefix}/ping")
    assert r.json() == {"ping": "pong"}
    assert r.status_code == status.HTTP_200_OK
