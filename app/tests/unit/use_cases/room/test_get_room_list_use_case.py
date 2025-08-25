import pytest
from unittest.mock import Mock

from app.src.use_cases.room.get_room_list_use_case import GetRoomListUseCase, RoomListResult


@pytest.fixture
def mock_room_repo():
    return Mock()


@pytest.fixture
def use_case(mock_room_repo):
    return GetRoomListUseCase(room_repository=mock_room_repo)


def test_get_room_list_use_case_build(use_case, mock_room_repo):
    assert use_case is not None
    assert use_case.room_repository == mock_room_repo


def test_get_room_list_use_case_success(use_case, mock_room_repo, sample_rooms_factory):
    sample_rooms = sample_rooms_factory(1, 21)

    mock_room_repo.select_rooms.return_value = sample_rooms[:10]
    mock_room_repo.count_all_rooms.return_value = 20

    result: RoomListResult = use_case.execute(offset=0, limit=10)

    assert result.total == 20
    assert result.offset == 0
    assert result.limit == 10
    assert result.order_by == "created_at"
    assert result.order_direction == "asc"
    assert isinstance(result.rooms, list)
    assert result.rooms == sample_rooms[:10]
    assert len(result.rooms) == 10

    mock_room_repo.select_rooms.assert_called_once_with(0, 10)
    mock_room_repo.count_all_rooms.assert_called_once()


def test_get_room_list_use_case_with_offset(use_case, mock_room_repo, sample_rooms_factory):
    sample_rooms = sample_rooms_factory(1, 21)

    mock_room_repo.select_rooms.return_value = sample_rooms[10:20]
    mock_room_repo.count_all_rooms.return_value = 20

    result: RoomListResult = use_case.execute(offset=10, limit=10)

    assert result.total == 20
    assert result.offset == 10
    assert result.limit == 10
    assert result.rooms == sample_rooms[10:20]
    assert len(result.rooms) == 10

    mock_room_repo.select_rooms.assert_called_once_with(10, 10)


def test_get_room_list_use_case_with_default_limit(use_case, mock_room_repo, sample_rooms_factory):
    sample_rooms = sample_rooms_factory(1, 30)

    mock_room_repo.select_rooms.return_value = sample_rooms[:20]
    mock_room_repo.count_all_rooms.return_value = 29

    result: RoomListResult = use_case.execute(offset=None, limit=None)

    assert result.total == 29
    assert result.offset == 0
    assert result.limit == 20
    assert result.rooms == sample_rooms[:20]
    assert len(result.rooms) == 20

    mock_room_repo.select_rooms.assert_called_once_with(0, 20)


def test_end():
    print("\n\nEnd => Get Room list usecase\n")
