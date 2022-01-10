from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser

from app.core.config import settings

auth = Cognito(
    region=settings.aws_region, userPoolId=settings.userpool_id, client_id=settings.app_client_id
)


get_current_user = CognitoCurrentUser(
    region=settings.aws_region, userPoolId=settings.userpool_id, client_id=settings.app_client_id
)
