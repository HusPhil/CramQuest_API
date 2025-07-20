from pydantic import BaseModel, Field, EmailStr, field_validator, validator
from app.models.player_model import PlayerTitle
from app.models.profile_model import Mood
from typing import Optional

from app.schemas.player_schema import PlayerRead
from app.schemas.profile_schema import ProfileRead
from app.schemas.user_schema import UserRead


class SignUpRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=12,
        strip_whitespace=True,
    )
    email: EmailStr
    password: str = Field(..., min_length=8)
    avatar_url: Optional[str] = Field(default=None)

    @field_validator("username")
    def username_no_spaces_and_valid_chars(cls, v):
        import re

        if not re.match(r"^[a-zA-Z0-9]+$", v):
            raise ValueError("Username must only contain a-z, A-Z, 0-9 and no spaces.")
        return v


class UserInfo(BaseModel):
    id: int
    username: str
    email: EmailStr


class PlayerInfo(BaseModel):
    id: int


class ProfileInfo(BaseModel):
    id: int
    avatar_url: Optional[str]


class AuthenticationResponse(BaseModel):
    user_info: UserInfo
    player: PlayerInfo
    profile: ProfileInfo
    access_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    user_session_info: UserRead
    player_session_info: PlayerRead
    profile_session_info: ProfileRead
