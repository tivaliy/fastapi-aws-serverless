from typing import List, Optional

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser

from app.core.config import get_app_settings
from app.core.settings.app import AppSettings


async def auth(request: Request) -> Cognito:
    """
    Fetches Cognito Auth from the App context.
    """
    return request.app.state.auth


async def admin_scoped_auth(
    cognito_auth: Cognito = Depends(auth),
    http_auth: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
) -> List[str]:
    cognito_auth.scope_name = ["admins"]
    return await cognito_auth(http_auth)


async def get_current_user(
    settings: AppSettings = Depends(get_app_settings),
    http_auth: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
) -> CognitoCurrentUser:
    current_user_auth = CognitoCurrentUser(
        region=settings.aws_region,
        userPoolId=settings.userpool_id,
        client_id=settings.app_client_id,
    )
    # Set custom Cognito claims class with extra attributes
    current_user_auth.user_info = settings.user_info_class
    return await current_user_auth(http_auth)
