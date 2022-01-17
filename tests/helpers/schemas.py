from pydantic import BaseModel, Field


class UserAuth(BaseModel):
    id_token: str = Field(..., alias="IdToken")
    access_token: str = Field(..., alias="AccessToken")
    refresh_token: str = Field(..., alias="RefreshToken")
    expires_in: str = Field(..., alias="ExpiresIn")
