from os import environ
from typing import Dict

import boto3
import pytest
from botocore.client import BaseClient
from fastapi import FastAPI
from fastapi.testclient import TestClient
from moto import mock_cognitoidp

from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.tests.helpers.utils import random_email, random_lower_string

# Set "test" settings environment
environ["APP_ENV"] = "test"


@pytest.fixture(scope="session")
def aws_credentials():
    environ["AWS_ACCESS_KEY_ID"] = "testing"
    environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    environ["AWS_SECURITY_TOKEN"] = "testing"
    environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="session")
def cognito_idp_client(aws_credentials, region_name: str = "us-east-1") -> BaseClient:
    with mock_cognitoidp():
        yield boto3.client("cognito-idp", region_name=region_name)


@pytest.fixture(scope="session")
def pool_name() -> str:
    return "fake-cognito-user-pool"


@pytest.fixture(scope="session")
def user_pool_id(cognito_idp_client: BaseClient, pool_name: str) -> str:
    response = cognito_idp_client.create_user_pool(PoolName=pool_name, UsernameAttributes=["email"])
    return response["UserPool"]["Id"]


@pytest.fixture(scope="session")
def app_client_id(cognito_idp_client: BaseClient, user_pool_id: str, pool_name: str) -> str:
    return cognito_idp_client.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=pool_name, GenerateSecret=False
    )["UserPoolClient"]["ClientId"]


@pytest.fixture
def test_user_auth_data(
    cognito_idp_client: BaseClient, user_pool_id: str, app_client_id: str
) -> Dict[str, str]:
    username = random_email()
    password = random_lower_string()

    cognito_idp_client.sign_up(ClientId=app_client_id, Username=username, Password=password)
    cognito_idp_client.admin_confirm_sign_up(UserPoolId=user_pool_id, Username=username)
    return {"USERNAME": username, "PASSWORD": password}


@pytest.fixture
def auth_results(cognito_idp_client: BaseClient, app_client_id: str, test_user_auth_data) -> Dict:
    return cognito_idp_client.initiate_auth(
        ClientId=app_client_id,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters=test_user_auth_data,
    )["AuthenticationResult"]


@pytest.fixture
def id_token(auth_results) -> str:
    return auth_results["IdToken"]


@pytest.fixture
def access_token(auth_results) -> str:
    return auth_results["AccessToken"]


@pytest.fixture
def initialized_app(
    monkeypatch, cognito_idp_client: BaseClient, user_pool_id: str, app_client_id: str
) -> FastAPI:

    # Set environment variables for proper Cognito setup
    monkeypatch.setenv("AWS_REGION", cognito_idp_client.meta.region_name)
    monkeypatch.setenv("USERPOOL_ID", user_pool_id)
    monkeypatch.setenv("APP_CLIENT_ID", app_client_id)

    from app.main import create_application  # local import for testing purpose

    return create_application()


@pytest.fixture
def settings() -> AppSettings:
    return get_app_settings()


@pytest.fixture
def client(initialized_app: FastAPI) -> TestClient:
    with TestClient(app=initialized_app) as c:
        yield c
