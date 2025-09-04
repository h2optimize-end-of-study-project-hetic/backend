import pytest

from unittest.mock import Mock

from app.src.use_cases.room.delete_room_use_case import DeleteRoomUseCase
from app.src.domain.interface_repositories.room_repository import RoomRepository


@pytest.fixture
def mock_room_repo():
    return Mock(spec=RoomRepository)


@pytest.fixture
def use_case(mock_room_repo):
    return DeleteRoomUseCase(room_repository=mock_room_repo)


def test_delete_room_use_case_build(use_case, mock_room_repo):
    assert use_case is not None
    assert use_case.room_repository == mock_room_repo


def test_delete_room_use_case_execute_success(use_case, mock_room_repo):
    room_id = 56
    mock_room_repo.delete_room.return_value = True

    result = use_case.execute(room_id)

    mock_room_repo.delete_room.assert_called_once_with(room_id)
    assert result is True


def test_delete_room_use_case_execute_failure(use_case, mock_room_repo):
    room_id = 72
    mock_room_repo.delete_room.return_value = False

    result = use_case.execute(room_id)

    mock_room_repo.delete_room.assert_called_once_with(room_id)
    assert result is False


def test_end():
    print("\n\nEnd => Delete Room usecase\n")
