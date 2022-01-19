from typing import List, Type

import pytest
from fastapi.testclient import TestClient
from fastapi_cloudauth.cognito import CognitoClaims
from pydantic import BaseModel
from starlette import status

from app.core.settings.app import AppSettings
from tests.helpers.schemas import CustomCognitoClaims, UserAuth
from tests.helpers.users import FAKE_USER_LIST


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


@pytest.mark.parametrize(
    "user_info_class, claims_attributes",
    [
        (CognitoClaims, {"email", "cognito:username"}),
        (CustomCognitoClaims, {"nickname", "email", "cognito:username"}),
    ],
)
def test_user_can_retrieve_own_profile(
    monkeypatch,
    client: TestClient,
    user_auth: UserAuth,
    settings: AppSettings,
    user_info_class: Type[BaseModel],
    claims_attributes: List[str],
) -> None:

    settings.user_info_class = user_info_class

    r = client.get(
        f"{settings.api_v1_prefix}/users/me",
        headers={"Authorization": f"{settings.jwt_token_prefix} {user_auth.id_token}"},
    )
    assert r.status_code == status.HTTP_200_OK
    assert claims_attributes <= r.json().keys()


def test_regular_user_can_not_list_users(
    client: TestClient, user_auth: UserAuth, settings: AppSettings
) -> None:
    r = client.get(
        f"{settings.api_v1_prefix}/users",
        headers={"Authorization": f"{settings.jwt_token_prefix} {user_auth.access_token}"},
    )
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_admin_user_can_list_users(
    client: TestClient, admin_user_auth: UserAuth, settings: AppSettings
) -> None:
    r = client.get(
        f"{settings.api_v1_prefix}/users",
        headers={"Authorization": f"{settings.jwt_token_prefix} {admin_user_auth.access_token}"},
    )
    assert r.status_code == status.HTTP_200_OK
    assert r.json() == FAKE_USER_LIST
