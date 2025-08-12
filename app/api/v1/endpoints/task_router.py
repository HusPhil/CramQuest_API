from fastapi import APIRouter, Body, Depends

from app.core.auth import get_current_user
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.task_crud import crud_end_task, crud_start_task, crud_sync_task_timings
from app.schemas.task_schema import TaskRead, TaskTimingBatchPayload


router = APIRouter(dependencies=[Depends(get_session), Depends(get_current_user)])
# router = APIRouter(dependencies=[Depends(get_session)])


@router.post("/{task_id}/start", response_model=TaskRead)
async def start_task(task_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_start_task(session, task_id)


@router.post("/{task_id}/end", response_model=TaskRead)
async def start_task(task_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_end_task(session, task_id)


@router.post("/sync_task_timings")
async def sync_task_timings(
    task_timing_batch_payload: TaskTimingBatchPayload = Body(
        ...,
        example={
            "70": {
                "start_time": "2025-06-29T07:19:44.657Z",
                "end_time": "2025-06-29T07:19:44.657Z",
                "description": "string",
            },
            "71": {
                "start_time": "2025-06-29T07:19:44.657Z",
                "end_time": "2025-06-29T07:19:44.657Z",
                "description": "string",
            },
            "72": {
                "start_time": "2025-06-29T07:19:44.657Z",
                "end_time": "2025-06-29T07:19:44.657Z",
                "description": "string",
            },
        },
        description="Keys are task IDs, values are timing objects",
    ),
    session: AsyncSession = Depends(get_session),
):
    print(task_timing_batch_payload)
    return await crud_sync_task_timings(session, task_timing_batch_payload)
