import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.domain.entities.building import Building
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.building.delete_building_use_case import DeleteBuildingUseCase
from app.src.use_cases.building.update_building_use_case import UpdateBuildingUseCase
from app.src.use_cases.building.create_building_use_case import CreateBuildingUseCase
from app.src.use_cases.building.get_building_list_use_case import GetBuildingListUseCase
from app.src.use_cases.building.get_building_by_id_use_case import GetBuildingByIdUseCase
from app.src.presentation.api.common.generic_model import PaginationMetadataModel
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.presentation.api.building.building_model import (
    PaginatedListBuildingModelResponse,
    BuildingCreateModelRequest,
    BuildingModelResponse,
    BuildingUpdateModelRequest,
)
from app.src.presentation.dependencies import (
    create_building_use_case,
    delete_building_use_case,
    get_building_by_id_use_case,
    get_building_list_use_case,
    update_building_use_case,
)
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

building_not_found = OpenApiErrorResponseConfig(code=404, description="Building not found", detail="Building with ID '123' not found")
building_already_exist = OpenApiErrorResponseConfig(
    code=409, description="Building already exists", detail="Building with ID '123' already exist"
)
creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Failed to create Building")
update_error = OpenApiErrorResponseConfig(code=406, description="Update fails", detail="Failed to update Building")
deletion_error = OpenApiErrorResponseConfig(code=406, description="Deletion fails", detail="Failed to delete Building")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")


logger = logging.getLogger(__name__)
building_router = APIRouter(
    prefix=f"/{OpenApiTags.building.value}", tags=[OpenApiTags.building]
)  # buildings and OpenApiBuildings are not bind to the entity building. It's just the param of APIRouter


@building_router.post(
    "",
    summary="Create a new building",
    response_model=BuildingModelResponse,
    response_description="Details of the created building",
    responses=generate_responses([building_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_building(
    use_case: Annotated[CreateBuildingUseCase, Depends(create_building_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    building: Annotated[BuildingCreateModelRequest, Body(embed=True)],

):
    """
    Create a new building

    - **name** : The name of the building
    - **description** : The purpose of the building
    - **room_count**: The number of room in the building
    - **street_number**: The address number of the building
    - **street_name**: The address of the building
    - **postal_code**: The postal code of the building
    - **city**: The city of where the building is
    - **country**: The country of where the building is
    - **latitude**: The latitude of the building
    - **longitude**: The longitude of the building

    """
    try:
        building_entity = Building(
            id=None,
            name=building.name,
            description=building.description,
            room_count=building.room_count,
            street_number=building.street_number,
            street_name=building.street_name,
            postal_code=building.postal_code,
            city=building.city,
            country=building.country,
            latitude=building.latitude,
            longitude=building.longitude,
            created_at=None,
            updated_at=None,
        )

        new_building: Building = use_case.execute(building_entity)

        return BuildingModelResponse(**new_building.to_dict())

    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@building_router.get(
    "",
    summary="Retrieve a list of buildings",
    response_model=PaginatedListBuildingModelResponse,
    response_description="Detailed information of the requested buildings",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_building_list(
    use_case: Annotated[GetBuildingListUseCase, Depends(get_building_list_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int | None = Query(20, ge=1, description="Number of elements return"),
):
    """
    Retrieve a list of buildings

    - **cursor**: Optional cursor for pagination (returns buildings with id >= cursor)
    - **limit**: Number of buildings to return (default: 20)
    """
    try:
        result = use_case.execute(cursor, limit)

        building_models = [BuildingModelResponse(**building.to_dict()) for building in result.buildings]

        metadata = PaginationMetadataModel(
            total=result.total,
            chunk_size=result.chunk_size,
            chunk_count=result.chunk_count,
            current_cursor=result.current_cursor,
            first_cursor=result.first_cursor,
            last_cursor=result.last_cursor,
            next_cursor=result.next_cursor,
        )

        response = PaginatedListBuildingModelResponse(data=building_models, metadata=metadata)

        return response

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@building_router.get(
    "/{building_id}",
    summary="Retrieve building info by ID",
    response_model=BuildingModelResponse,
    response_description="Detailed information of the requested building",
    responses=generate_responses([building_not_found, unexpected_error]),
    deprecated=False,
)
async def read_building(
    use_case: Annotated[GetBuildingByIdUseCase, Depends(get_building_by_id_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    building_id: int = Path(..., ge=1, description="The building ID (positive integer)"),
):
    """
    Retrieve a building by its unique identifier

    - **building_id**: Must be a positive integer (≥ 1)
    """
    try:
        building_entity: Building = use_case.execute(building_id)

        return BuildingModelResponse(**building_entity.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@building_router.patch(
    "/{building_id}",
    summary="Update a building partially",
    response_model=BuildingModelResponse,
    responses=generate_responses([building_not_found, building_already_exist, unexpected_error]),
)
async def update_building(
    use_case: Annotated[UpdateBuildingUseCase, Depends(update_building_use_case)],
    building: Annotated[BuildingUpdateModelRequest, Body(embed=True)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    building_id: int = Path(..., ge=1, description="ID of the building to update"),
):
    try:
        update_data = building.model_dump(exclude_unset=True)
        updated_building = use_case.execute(building_id, update_data)

        return BuildingModelResponse(**updated_building.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except UpdateFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@building_router.delete(
    "/{building_id}",
    summary="Delete a building by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses([building_not_found, deletion_error, unexpected_error]),
)
async def delete_building(
    use_case: Annotated[DeleteBuildingUseCase, Depends(delete_building_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    building_id: int = Path(..., ge=1, description="ID of the building to delete"),
):
    try:
        use_case.execute(building_id)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Failed to execute request on Building"
        ) from e
    except DeletionFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
