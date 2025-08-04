from os import access
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import Security
from app.core.auth import create_access_token, create_refresh_token

from app.models.user_model import User
from app.schemas.player_schema import PlayerRead

from app.schemas.profile_schema import ProfileRead

from app.crud.auth_crud import crud_sign_up_user
from app.schemas.auth_schema import RefreshTokenResponse, SignUpRequest

from app.crud.user_crud import crud_read_user_by_username, crud_read_user_complete_info
from app.schemas.user_schema import UserRead


from jose import JWTError, ExpiredSignatureError

refresh_token_cookie_key = "_Host-cramquest_ssfpwrtk"

router = APIRouter()


class InvalidCredential(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid username or password")


@router.post("/sign_in")
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> JSONResponse:

    try:
        user = await crud_read_user_by_username(session, username=form_data.username)
        print(user)

    except:
        raise InvalidCredential

    if not user:
        raise InvalidCredential

    if not Security.verify_hash(form_data.password, user.password):
        raise InvalidCredential

    response = _get_authentication_response(user, user.player)

    return response


@router.post("/sign_up")
async def sign_up(
    request: Request,
    sign_up_request: SignUpRequest,
    session: Session = Depends(get_session),
) -> JSONResponse:
    new_user, new_player = await crud_sign_up_user(session, sign_up_request)
    response = _get_authentication_response(new_user, new_player)
    return response


@router.post("/sign_out")
async def sign_out() -> JSONResponse:
    response = JSONResponse(content={"message": "Successfully signed out"})

    response.delete_cookie(
        key=refresh_token_cookie_key,
        secure=False,
        path="/",
        samesite="lax",
        httponly=True,
    )

    return response


@router.post("/refresh_session")
async def refresh_session(request: Request, session: Session = Depends(get_session)):
    refresh_token = request.cookies.get(refresh_token_cookie_key)
    print("Refresh token:", refresh_token)

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        token_verification_res = Security.verify_refresh_token(refresh_token)

        user_id = token_verification_res.user_id
        player_id = token_verification_res.player_id

        user_complete_info = await crud_read_user_complete_info(session, int(user_id))
        print(user_complete_info)

    except ExpiredSignatureError:
        print("ExpiredSignatureError")
        raise HTTPException(status_code=403, detail="Refresh token expired")
    except JWTError:
        print("JWTError")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({"user_id": user_id, "player_id": player_id})

    user_session_info, player_session_info, profile_session_info = build_user_bundle(
        user_complete_info
    )

    return RefreshTokenResponse(
        access_token=new_access_token,
        user_session_info=user_session_info,
        player_session_info=player_session_info,
        profile_session_info=profile_session_info,
    )


def _get_authentication_response(user: UserRead, player: PlayerRead) -> JSONResponse:

    refresh_token = create_refresh_token(
        {"user_id": str(user.id), "player_id": str(player.id)}
    )

    access_token = (
        create_access_token({"user_id": str(user.id), "player_id": str(player.id)}),
    )

    response = JSONResponse(
        content={
            "access_token": access_token,
            "message": "Sucessfully signed in",
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    )

    response.set_cookie(
        key=refresh_token_cookie_key,
        value=refresh_token,
        httponly=True,
        secure=not True,  # True in production with HTTPS
        samesite="lax",  # or "strict" or "none"
        path="/",  # Send this cookie to all routes
    )

    return response


def build_user_bundle(user_complete_info: User):
    """Bundle User, Player, and Profile Read schemas."""

    user_read = UserRead(
        id=user_complete_info.id,
        email=user_complete_info.email,
        username=user_complete_info.username,
        is_admin=user_complete_info.is_admin,
        is_active=user_complete_info.is_active,
    )

    player_read = PlayerRead(
        id=user_complete_info.player.id,
        user_id=user_complete_info.player.user_id,
        level=user_complete_info.player.level,
        experience=user_complete_info.player.experience,
        next_level_xp=user_complete_info.player.next_level_xp,
        title=user_complete_info.player.title,
        boss_availability_counter=user_complete_info.player.boss_availability_counter,
        daily_streak=user_complete_info.player.daily_streak,
        session_streak=user_complete_info.player.session_streak,
        longest_daily_streak=user_complete_info.player.longest_daily_streak,
        longest_session_streak=user_complete_info.player.longest_session_streak,
        weekly_streak=user_complete_info.player.weekly_streak,
        longest_weekly_streak=user_complete_info.player.longest_weekly_streak,
        last_checkin_date=user_complete_info.player.last_checkin_date,
        last_week_checkin_date=user_complete_info.player.last_week_checkin_date,
    )

    profile_read = ProfileRead(
        id=user_complete_info.player.profile.id,
        player_id=user_complete_info.player.profile.player_id,
        avatar_url=user_complete_info.player.profile.avatar_url,
        bio=user_complete_info.player.profile.bio,
        mood=user_complete_info.player.profile.mood,
        skin_url=user_complete_info.player.profile.skin_url,
    )

    return user_read, player_read, profile_read
