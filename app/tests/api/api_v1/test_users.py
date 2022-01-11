import pytest
from fastapi.testclient import TestClient
from starlette import status

from app.core.config import settings


@pytest.fixture(params=("", "value", "Token value", "JWT value", "Bearer value"))
def wrong_authorization_header(request) -> str:
    return request.param


def test_user_can_not_access_own_profile_if_not_logged_in(client: TestClient) -> None:
    r = client.get(f"{settings.api_v1_prefix}/users/me")
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_can_not_retrieve_own_profile_if_wrong_token(
    client: TestClient, wrong_authorization_header: str
) -> None:
    r = client.get(
        f"{settings.api_v1_prefix}/users/me", headers={"Authorization": wrong_authorization_header}
    )
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
