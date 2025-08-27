import pytest

from unittest.mock import Mock

from app.src.use_cases.room.create_room_use_case import CreateRoomUseCase
from app.src.domain.interface_repositories.room_repository import RoomRepository


@pytest.fixture
def mock_room_repo():
    return Mock(spec=RoomRepository)


@pytest.fixture
def use_case(mock_room_repo):
    return CreateRoomUseCase(room_repository=mock_room_repo)


def test_create_room_use_case_build(use_case, mock_room_repo):
    assert use_case is not None
    assert use_case.room_repository == mock_room_repo


def test_create_room_use_case_execute_success(use_case, mock_room_repo, sample_rooms_factory):
    fake_room = sample_rooms_factory(1, 2)[0]
    mock_room_repo.create_room.return_value = fake_room

    result = use_case.execute(fake_room)

    mock_room_repo.create_room.assert_called_once_with(fake_room)
    assert result == fake_room


def test_end():
    print("\n\nEnd => Create Room usecase\n")


