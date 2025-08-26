import pytest

from unittest.mock import Mock

from app.src.domain.entities.room import Room
from app.src.use_cases.room.update_room_use_case import UpdateRoomUseCase
from app.src.domain.interface_repositories.room_repository import RoomRepository


@pytest.fixture
def mock_room_repo():
    return Mock(spec=RoomRepository)


@pytest.fixture
def use_case(mock_room_repo):
    return UpdateRoomUseCase(room_repository=mock_room_repo)


def test_update_room_use_case_build(use_case, mock_room_repo):
    assert use_case is not None
    assert use_case.room_repository == mock_room_repo


def test_update_room_use_case_execute_success(use_case, mock_room_repo, sample_rooms_factory):
    fake_room = sample_rooms_factory(1, 2)[0]

    room_id = 1
    room_data = {"name": "updated name", "description": "updated description"}

    updated_room = Room(
        id= 1,
        name= "string",
        description= "string",
        floor= 0,
        building_id= 1,
        area= 1,
        shape= [
        [
            0
        ]
        ],
        capacity= 0,
        created_at="2025-08-25T10:52:33.001Z", 
        start_at="2025-08-25T10:52:33.001Z",
        end_at="2025-08-25T10:52:33.001Z",
        updated_at="2025-08-25T10:52:33.001Z" 
    )

    mock_room_repo.update_room.return_value = updated_room

    result = use_case.execute(room_id, room_data)

    mock_room_repo.update_room.assert_called_once_with(room_id, room_data)
    assert result == updated_room


def test_end():
    print("\n\nEnd => Update Room usecase\n")
