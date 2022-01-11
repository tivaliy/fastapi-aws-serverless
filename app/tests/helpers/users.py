import uuid

from app.schemas import User
from app.tests.helpers.utils import random_email


def create_random_user() -> User:
    email = random_email()
    user = User(id=str(uuid.uuid4()), email=email)
    return user
