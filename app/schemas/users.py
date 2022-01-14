from typing import Optional

from pydantic import BaseModel, Field


# Shared properties
class UserBase(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserInDBBase(UserBase):
    id: str = None


# Additional properties to return via API
class User(UserInDBBase):
    pass


class UserAuth(BaseModel):
    id_token: str = Field(..., alias="IdToken")
    access_token: str = Field(..., alias="AccessToken")
    refresh_token: str = Field(..., alias="RefreshToken")
    expires_in: str = Field(..., alias="ExpiresIn")
