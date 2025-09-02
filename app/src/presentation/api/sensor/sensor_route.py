from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.presentation.dependencies import get_sensor_repo, SQLSensorRepository

sensor_dyn_router = APIRouter(prefix="/sensors", tags=[OpenApiTags.sensor])

@sensor_dyn_router.get("/{kind}/latest")
def latest(kind: str = Path(...), repo: Annotated[SQLSensorRepository, Depends(get_sensor_repo)] = None):
    row = repo.get_latest()
    return row.model_dump() if hasattr(row, "model_dump") and row else None

@sensor_dyn_router.get("/{kind}")
def list_readings(
    kind: str = Path(...),
    limit: int = Query(100, ge=1, le=1000),
    repo: Annotated[SQLSensorRepository, Depends(get_sensor_repo)] = None,
):
    rows = repo.get_all(limit=limit)
    return [r.model_dump() for r in rows]

@sensor_dyn_router.get("/{kind}/range")
def range_readings(
    kind: str = Path(...),
    start: datetime = Query(...),
    end: datetime = Query(...),
    limit: int | None = Query(None, ge=1, le=10000),
    repo: Annotated[SQLSensorRepository, Depends(get_sensor_repo)] = None,
):
    rows = repo.get_range(start, end, limit=limit)
    return [r.model_dump() for r in rows]
