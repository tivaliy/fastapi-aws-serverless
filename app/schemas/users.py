from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserInDBBase(UserBase):
    id: Optional[str] = None


# Additional properties to return via API
class User(UserInDBBase):
    pass
