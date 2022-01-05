from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import CognitoClaims

from app.api.deps import get_current_user

router = APIRouter()


@router.get("/me", response_model=CognitoClaims)
def read_user_me(current_user: CognitoClaims = Depends(get_current_user)) -> CognitoClaims:
    return current_user
