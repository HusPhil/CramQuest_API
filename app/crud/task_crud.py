from datetime import datetime, timezone
from email.policy import HTTP
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy import text
from app.models.task_model import Task
from app.schemas.task_schema import TaskRead, TaskTimingBatchPayload


async def crud_start_task(session: AsyncSession, task_id: int) -> TaskRead:
    try:
        task_to_update = await _get_task_or_404(session, task_id)
        task_to_update.start_time = datetime.now(timezone.utc)
        await session.commit()
        return _serialize_task(task_to_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def crud_end_task(session: AsyncSession, task_id: int) -> TaskRead:
    try:
        task_to_update = await _get_task_or_404(session, task_id)
        task_to_update.end_time = datetime.now(timezone.utc)
        await session.commit()
        return _serialize_task(task_to_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def crud_sync_task_timings(
    session: AsyncSession, task_timing_batch_payload: TaskTimingBatchPayload
):
    payload = task_timing_batch_payload.root
    if not payload:
        return {"status": "empty payload"}

    try:
        task_ids = list(payload.keys())

        case_start = "CASE id "
        case_end = "CASE id "
        params = {}

        for task_id, timing in payload.items():
            case_start += f"WHEN {task_id} THEN CAST(:start_{task_id} AS TIMESTAMPTZ) "
            case_end += f"WHEN {task_id} THEN CAST(:end_{task_id} AS TIMESTAMPTZ) "
            params[f"start_{task_id}"] = timing.start_time
            params[f"end_{task_id}"] = timing.end_time

        case_start += "END"
        case_end += "END"

        # SAFER PARAMETERIZED WHERE IN
        placeholders = [f":id_{i}" for i in task_ids]
        for task_id in task_ids:
            params[f"id_{task_id}"] = task_id
        where_clause = ", ".join(placeholders)

        query = text(
            f"""
            UPDATE task
            SET
                start_time = {case_start},
                end_time = {case_end}
            WHERE id IN ({where_clause})
        """
        )

        print(query)

        await session.execute(query, params)
        await session.commit()

        print("updated", len(task_ids))

        return task_timing_batch_payload.root

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


async def _get_task_or_404(session: AsyncSession, task_id: int) -> Task:
    statement = select(Task).where(Task.id == task_id)

    task = await session.scalar(statement)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


def _serialize_task(task: Task) -> TaskRead:

    return TaskRead(
        id=task.id,
        start_time=task.start_time,
        end_time=task.end_time,
        description=task.description,
        study_session_id=task.study_session_id,
    )
