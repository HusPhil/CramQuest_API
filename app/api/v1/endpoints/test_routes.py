from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from sqlalchemy import text

from app.services.game_service import GameService

router = APIRouter()


@router.get("/debug/foreign_keys/")
def check_foreign_keys(session: Session = Depends(get_session)):
    result = session.exec(text("PRAGMA foreign_keys;")).fetchone()
    return {"foreign_keys_enabled": bool(result[0])}


@router.get("/debug/gameservice/next_level_xp/{current_level}")
def check_next_level_xp(current_level: int, session: Session = Depends(get_session)):
    next_level_xp = GameService.next_level_xp(current_level)
    return {next_level_xp}
