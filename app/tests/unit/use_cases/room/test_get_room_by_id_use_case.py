import pytest
from unittest.mock import Mock

from app.src.use_cases.room.get_room_by_id_use_case import GetRoomByIdUseCase
from app.src.domain.interface_repositories.room_repository import RoomRepository


@pytest.fixture
def mock_room_repo():
    return Mock(spec=RoomRepository)


@pytest.fixture
def use_case(mock_room_repo):
    return GetRoomByIdUseCase(room_repository=mock_room_repo)


def test_get_room_by_id_use_case_build(use_case, mock_room_repo):
    assert use_case is not None
    assert use_case.room_repository == mock_room_repo


def test_get_room_by_id_use_case_execute_success(use_case, mock_room_repo, sample_rooms_factory):
    fake_room = sample_rooms_factory(1, 2)[0]
    room_id = 1

    mock_room_repo.select_room_by_id.return_value = fake_room

    result = use_case.execute(room_id)

    mock_room_repo.select_room_by_id.assert_called_once_with(room_id)

    assert result == fake_room


def test_end():
    print("\n\nEnd => Get Room by ID usecase\n")
