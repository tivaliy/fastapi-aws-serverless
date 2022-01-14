import pytest
from fastapi.testclient import TestClient
from fastapi_cloudauth.cognito import CognitoCurrentUser
from starlette import status

from app.core.settings.app import AppSettings
from tests.helpers.users import FAKE_USER_LIST, PatchedCognitoClaims


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
    monkeypatch, client: TestClient, user_auth, settings: AppSettings
) -> None:

    # The moto library doesn't support "cognito:username" claim in idToken and token validation
    # process fails. Let's patch CognitoClaims to define username field with default value
    with monkeypatch.context() as m:
        m.setattr(CognitoCurrentUser, "user_info", PatchedCognitoClaims)
        r = client.get(
            f"{settings.api_v1_prefix}/users/me",
            headers={"Authorization": f"{settings.jwt_token_prefix} {user_auth.id_token}"},
        )
    assert r.status_code == status.HTTP_200_OK


def test_regular_user_can_not_list_users(
    client: TestClient, user_auth, settings: AppSettings
) -> None:
    r = client.get(
        f"{settings.api_v1_prefix}/users",
        headers={"Authorization": f"{settings.jwt_token_prefix} {user_auth.access_token}"},
    )
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_admin_user_can_list_users(
    client: TestClient, admin_user_auth, settings: AppSettings
) -> None:
    r = client.get(
        f"{settings.api_v1_prefix}/users",
        headers={"Authorization": f"{settings.jwt_token_prefix} {admin_user_auth.access_token}"},
    )
    assert r.status_code == status.HTTP_200_OK
    assert r.json() == FAKE_USER_LIST
