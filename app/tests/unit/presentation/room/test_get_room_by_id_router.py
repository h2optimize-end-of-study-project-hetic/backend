import pytest
from unittest.mock import Mock

from app.src.presentation.main import app
from app.src.common.exception import NotFoundError
from app.src.presentation.dependencies import get_room_by_id_use_case
from app.src.use_cases.room.get_room_by_id_use_case import GetRoomByIdUseCase


@pytest.fixture
def fake_room(sample_rooms_factory):
    return sample_rooms_factory(1, 2)[0]


@pytest.fixture
def mock_get_room_by_id_use_case(fake_room):
    mock = Mock(spec=GetRoomByIdUseCase)
    mock.execute.return_value = fake_room
    return mock


@pytest.fixture
def override_dependencies(mock_get_room_by_id_use_case):
    app.dependency_overrides[get_room_by_id_use_case] = lambda: mock_get_room_by_id_use_case
    yield
    app.dependency_overrides = {}


def test_get_room_by_id_success(client, override_dependencies, mock_get_room_by_id_use_case, fake_room):
    room_id = fake_room.id
    response = client.get(f"/api/v1/room/{room_id}")

    mock_get_room_by_id_use_case.execute.assert_called_once_with(room_id)
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == fake_room.id
    assert data["name"] == fake_room.name
    assert data["description"] == fake_room.description
    assert data["floor"] == fake_room.floor
    assert data["building_id"] == fake_room.building_id
    assert data["area"] == fake_room.area
    assert data["capacity"] == fake_room.capacity
    assert data["created_at"] == fake_room.created_at.isoformat()
    assert data["updated_at"] == fake_room.updated_at.isoformat()


def test_get_room_by_id_failed_not_found(client, override_dependencies, mock_get_room_by_id_use_case):
    room_id = 999
    mock_get_room_by_id_use_case.execute.side_effect = NotFoundError("Room", room_id)

    response = client.get(f"/api/v1/room/{room_id}")

    mock_get_room_by_id_use_case.execute.assert_called_once_with(room_id)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Room with ID '{room_id}' not found"


def test_end():
    print("\n\nEnd => Get Room by ID route\n")
