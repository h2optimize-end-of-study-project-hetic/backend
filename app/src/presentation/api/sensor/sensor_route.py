import logging
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.presentation.api.common.errors import (
    OpenApiErrorResponseConfig,
    generate_responses,
)
from app.src.presentation.dependencies import get_sensor_repo
from app.src.infrastructure.db.repositories.sensor_repository_sql import SQLSensorRepository

logger = logging.getLogger(__name__)

sensor_router = APIRouter(prefix="/sensors", tags=[OpenApiTags.sensor])

# --- Error configs
not_found_error = OpenApiErrorResponseConfig(
    code=404, description="Sensor not found", detail="Sensor with this ID was not found"
)
unexpected_error = OpenApiErrorResponseConfig(
    code=500, description="Unexpected error", detail="Internal server error"
)


# --- Routes dynamiques ---

@sensor_router.get(
    "/{kind}/latest",
    summary="Get the latest measurement for a given sensor type",
    responses=generate_responses([not_found_error, unexpected_error]),
)
def get_latest_sensor(
    kind: str = Path(..., description="Sensor kind (temperature, humidity, motion, etc.)"),
    repo: Annotated[SQLSensorRepository, Depends(get_sensor_repo)] = None,
):
    try:
        row = repo.get_latest()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found")
        return row.model_dump()
    except Exception as e:
        logger.error(f"Unexpected error while fetching latest {kind}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@sensor_router.get(
    "/{kind}",
    summary="List recent measurements for a given sensor type",
    responses=generate_responses([unexpected_error]),
)
def list_sensors(
    kind: str = Path(...),
    limit: int = Query(100, ge=1, le=1000),
    repo: Annotated[SQLSensorRepository, Depends(get_sensor_repo)] = None,
):
    try:
        rows = repo.get_all(limit=limit)
        return [r.model_dump() for r in rows]
    except Exception as e:
        logger.error(f"Unexpected error while fetching list for {kind}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@sensor_router.get(
    "/{kind}/range",
    summary="Get sensor data in a time range",
    responses=generate_responses([unexpected_error]),
)
def range_sensors(
    kind: str = Path(...),
    start: datetime = Query(..., description="Start datetime (ISO8601)"),
    end: datetime = Query(..., description="End datetime (ISO8601)"),
    limit: int | None = Query(None, ge=1, le=10000),
    repo: Annotated[SQLSensorRepository, Depends(get_sensor_repo)] = None,
):
    try:
        rows = repo.get_range(start, end, limit=limit)
        return [r.model_dump() for r in rows]
    except Exception as e:
        logger.error(f"Unexpected error while fetching range for {kind}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
