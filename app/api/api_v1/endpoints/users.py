from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app import schemas
from app.api.deps import admin_scoped_auth, get_current_user
from tests.helpers.users import FAKE_USER_LIST

router = APIRouter()


@router.get("", response_model=List[schemas.User], dependencies=[Depends(admin_scoped_auth)])
def read_users() -> List[schemas.User]:
    # Generate fake user list
    return FAKE_USER_LIST


@router.get("/me")
def read_user_me(
    current_user: BaseModel = Depends(get_current_user),
) -> Optional[Union[BaseModel, Dict[str, Any]]]:
    return current_user
