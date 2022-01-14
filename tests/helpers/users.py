import random
import uuid

from app.schemas import User
from tests.helpers.utils import random_email

FAKE_USER_LIST = [
    User(id=str(uuid.uuid4()), email=random_email()) for _ in range(random.randint(1, 5))
]
