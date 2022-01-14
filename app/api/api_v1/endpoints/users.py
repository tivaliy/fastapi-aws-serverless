from typing import List

from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import CognitoClaims

from app import schemas
from app.api.deps import admin_scoped_auth, get_current_user
from app.tests.helpers.users import FAKE_USER_LIST

router = APIRouter()


@router.get("", response_model=List[schemas.User], dependencies=[Depends(admin_scoped_auth)])
def read_users():
    # Generate fake user list
    return FAKE_USER_LIST


@router.get("/me", response_model=CognitoClaims)
def read_user_me(current_user: CognitoClaims = Depends(get_current_user)) -> CognitoClaims:
    return current_user
