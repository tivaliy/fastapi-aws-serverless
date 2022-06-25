from fastapi.testclient import TestClient
from starlette import status


def test_ping(client: TestClient) -> None:
    r = client.get("/ping")
    assert r.json() == {"ping": "pong"}
    assert r.status_code == status.HTTP_200_OK
