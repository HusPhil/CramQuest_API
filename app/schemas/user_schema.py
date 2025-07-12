from typing import Annotated
from typing import Optional
from pydantic import EmailStr, SecretStr, Field, BaseModel
from app.schemas.player_schema import PlayerRead


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, strip_whitespace=True)
    email: EmailStr


class UserRead(UserBase):
    id: int
    is_admin: bool
    is_active: bool


class UserPlayerRead(UserRead):
    player: PlayerRead


class UserCreate(UserBase):
    password: SecretStr


class UserUpdate(BaseModel):  # ✅ Schema for updating users (all fields optional)
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None
