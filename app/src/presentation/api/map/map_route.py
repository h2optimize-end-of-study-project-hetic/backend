import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status, UploadFile, File, Form

from datetime import datetime
import shutil, os

from app.src.domain.entities.map import Map
from app.src.presentation.core.open_api_maps import OpenApiMaps
from app.src.use_cases.map.delete_map_use_case import DeleteMapUseCase
from app.src.use_cases.map.update_map_use_case import UpdateMapUseCase
from app.src.use_cases.map.create_map_use_case import CreateMapUseCase
from app.src.use_cases.map.get_map_list_use_case import GetMapListUseCase
from app.src.use_cases.map.get_map_by_id_use_case import GetMapByIdUseCase
from app.src.presentation.api.common.generic_model import PaginationMetadataModel
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.presentation.api.map.map_model import (
    PaginatedListMapModelResponse,
    MapCreateModelRequest,
    MapModelResponse,
    MapUpdateModelRequest,
)
from app.src.presentation.dependencies import (
    create_map_use_case,
    delete_map_use_case,
    get_map_by_id_use_case,
    get_map_list_use_case,
    update_map_use_case,
)
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

map_not_found = OpenApiErrorResponseConfig(code=404, description="Map not found", detail="Map with ID '123' not found")
map_already_exist = OpenApiErrorResponseConfig(
    code=409, description="Map already exists", detail="Map with file_name 'Building A - Floor 1' already exists"
)
creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Failed to create Map")
update_error = OpenApiErrorResponseConfig(code=406, description="Update fails", detail="Failed to update Map")
deletion_error = OpenApiErrorResponseConfig(code=406, description="Deletion fails", detail="Failed to delete Map")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")


logger = logging.getLogger(__name__)
map_router = APIRouter(
    prefix=f"/{OpenApiMaps.map.value}", tags=[OpenApiMaps.map]
)  # maps and OpenApiMaps are not bind to the entity map. It's just the param of APIRouter


@map_router.post(
    "",
    summary="Create a new map",
    response_model=MapModelResponse,
    response_description="Details of the created map",
    responses=generate_responses([map_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_map(
    use_case: Annotated[CreateMapUseCase, Depends(create_map_use_case)],
    # map: Annotated[MapCreateModelRequest, Body(embed=True)],
    building_id: int = Form(...),
    width: int = Form(...),
    length: int = Form(...),
    file: UploadFile = File(...),
):
    """
    Create a new map
    - **building_id** : The building ID to which this map is attached to
    - **file_name**: Name of the map (minimum 3 characters, maximum 255 characters)
    - **path**: Location of the map
    - **width** : Width of the map image
    - **width** : Length of the map image
    """
    try:
        # save map image
        file_name = file.filename

        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))  
        maps_dir = os.path.join(PROJECT_ROOT, "maps")
        os.makedirs(maps_dir, exist_ok=True)

        save_path = os.path.join(maps_dir, file_name)
        print("Fichier sauvegardé dans :", save_path)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # create entity
        map_entity = Map(
            id=None,
            building_id=building_id,
            file_name=file_name,
            path="/code/app/maps",
            width=width,
            length=length,
            created_at=None,
            updated_at=None,
        )

        new_map: Map = use_case.execute(map_entity)

        return MapModelResponse(**new_map.to_dict())

    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@map_router.get(
    "",
    summary="Retrieve a list of maps",
    response_model=PaginatedListMapModelResponse,
    response_description="Detailed information of the requested maps",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_map_list(
    use_case: Annotated[GetMapListUseCase, Depends(get_map_list_use_case)],
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int | None = Query(20, ge=1, description="Number of elements return"),
):
    """
    Retrieve a list of maps

    - **cursor**: Optional cursor for pagination (returns maps with id >= cursor)
    - **limit**: Number of maps to return (default: 20)
    """
    try:
        result = use_case.execute(cursor, limit)

        map_models = [MapModelResponse(**map.to_dict()) for map in result.maps]

        metadata = PaginationMetadataModel(
            total=result.total,
            chunk_size=result.chunk_size,
            chunk_count=result.chunk_count,
            current_cursor=result.current_cursor,
            first_cursor=result.first_cursor,
            last_cursor=result.last_cursor,
            next_cursor=result.next_cursor,
        )

        response = PaginatedListMapModelResponse(data=map_models, metadata=metadata)

        return response

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@map_router.get(
    "/{map_id}",
    summary="Retrieve map by ID",
    response_model=MapModelResponse,
    response_description="Detailed information of the requested map",
    responses=generate_responses([map_not_found, unexpected_error]),
    deprecated=False,
)
async def read_map(
    use_case: Annotated[GetMapByIdUseCase, Depends(get_map_by_id_use_case)],
    map_id: int = Path(..., ge=1, description="The map ID (positive integer)"),
):
    """
    Retrieve a map by its unique identifier

    - **map_id**: Must be a positive integer (≥ 1)
    """
    try:
        map_entity: Map = use_case.execute(map_id)

        return MapModelResponse(**map_entity.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@map_router.patch(
    "/{map_id}",
    summary="Update a map partially",
    response_model=MapModelResponse,
    responses=generate_responses([map_not_found, map_already_exist, unexpected_error]),
)
async def update_map(
    use_case: Annotated[UpdateMapUseCase, Depends(update_map_use_case)],
    map: Annotated[MapUpdateModelRequest, Body(embed=True)],
    map_id: int = Path(..., ge=1, description="ID of the map to update"),
):
    try:
        update_data = map.model_dump(exclude_unset=True)
        updated_map = use_case.execute(map_id, update_data)

        return MapModelResponse(**updated_map.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except UpdateFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@map_router.delete(
    "/{map_id}",
    summary="Delete a map by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses([map_not_found, deletion_error, unexpected_error]),
)
async def delete_map(
    use_case: Annotated[DeleteMapUseCase, Depends(delete_map_use_case)],
    map_id: int = Path(..., ge=1, description="ID of the map to delete"),
):
    try:
        use_case.execute(map_id)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Failed to execute request on Map"
        ) from e
    except DeletionFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
