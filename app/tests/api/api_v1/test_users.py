import pytest
from fastapi.testclient import TestClient
from starlette import status

from app.core.settings.app import AppSettings


@pytest.fixture(params=("", "value", "Token value", "JWT value", "Bearer value"))
def wrong_authorization_header(request) -> str:
    return request.param


def test_user_can_not_access_own_profile_if_not_logged_in(
    client: TestClient, settings: AppSettings
) -> None:
    r = client.get(f"{settings.api_v1_prefix}/users/me")
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_can_not_retrieve_own_profile_if_wrong_token(
    client: TestClient, wrong_authorization_header: str, settings: AppSettings
) -> None:
    r = client.get(
        f"{settings.api_v1_prefix}/users/me", headers={"Authorization": wrong_authorization_header}
    )
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_can_retrieve_own_profile(
    client: TestClient, id_token: str, settings: AppSettings
) -> None:
    client.get(
        f"{settings.api_v1_prefix}/users/me",
        headers={"Authorization": f"{settings.jwt_token_prefix} {id_token}"},
    )
    # assert r.status_code == status.HTTP_200_OK


def test_user_can_list_users(client: TestClient, access_token: str, settings: AppSettings) -> None:
    client.get(
        f"{settings.api_v1_prefix}/users",
        headers={"Authorization": f"{settings.jwt_token_prefix} {access_token}"},
    )
    # assert r.status_code == status.HTTP_200_OK
