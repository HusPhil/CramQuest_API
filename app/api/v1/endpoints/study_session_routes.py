from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.auth import get_current_user
from app.models.user_model import User
from app.schemas.study_session_schema import (
    StudySessionEnd,
    StudySessionRead,
    StudySessionCreate,
)
from app.crud.study_session_crud import (
    crud_create_study_session,
    crud_read_study_session,
    crud_end_study_session,
    crud_read_all_study_sessions,
)

router = APIRouter()
# router = APIRouter(dependencies=[Depends(get_session), Depends(get_current_user)])


@router.post("/", response_model=StudySessionRead)
async def create_study_session(
    new_study_session: StudySessionCreate, session: AsyncSession = Depends(get_session)
):
    return await crud_create_study_session(session, new_study_session)


@router.get("/", response_model=list[StudySessionRead])
async def read_all_study_sessions(session: AsyncSession = Depends(get_session)):
    return await crud_read_all_study_sessions(session)


@router.get("/{study_session_id}", response_model=StudySessionRead)
async def read_study_session(
    study_session_id: int, session: AsyncSession = Depends(get_session)
):
    return await crud_read_study_session(session, study_session_id)


@router.post("/{study_session_id}/end", response_model=StudySessionEnd)
async def end_study_session(
    study_session_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await crud_end_study_session(session, study_session_id, current_user)
