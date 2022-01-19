import random
import uuid
from typing import Tuple

from botocore.client import BaseClient

from app.schemas import User
from tests.helpers.utils import random_email, random_lower_string

FAKE_USER_LIST = [
    User(id=str(uuid.uuid4()), email=random_email()) for _ in range(random.randint(1, 5))
]


def create_cognito_user(cognito_idp_client: BaseClient, app_client_id: str) -> Tuple[str, str, str]:
    nickname = random_lower_string(8)
    username = random_email()
    password = random_lower_string()

    cognito_idp_client.sign_up(
        ClientId=app_client_id,
        Username=username,
        Password=password,
        UserAttributes=[
            {"Name": "cognito:username", "Value": username},
            {"Name": "nickname", "Value": nickname},
        ],
    )
    return nickname, username, password
