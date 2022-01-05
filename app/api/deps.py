from fastapi_cloudauth.cognito import CognitoCurrentUser

from app.core.config import get_app_settings

settings = get_app_settings()


get_current_user = CognitoCurrentUser(
    region=settings.aws_region, userPoolId=settings.userpool_id, client_id=settings.app_client_id
)
