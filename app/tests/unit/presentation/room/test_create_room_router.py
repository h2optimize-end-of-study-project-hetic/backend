import pytest
from unittest.mock import Mock
from app.src.presentation.main import app
from app.src.domain.entities.room import Room
from app.src.presentation.dependencies import create_room_use_case
from app.src.use_cases.room.create_room_use_case import CreateRoomUseCase
from app.src.common.exception import CreationFailedError


@pytest.fixture
def fake_room(sample_rooms_factory):
    return sample_rooms_factory(1, 2)[0]


@pytest.fixture
def mock_create_room_use_case(fake_room):
    mock = Mock(spec=CreateRoomUseCase)
    mock.execute.return_value = fake_room
    return mock


@pytest.fixture
def override_dependencies(mock_create_room_use_case):
    app.dependency_overrides[create_room_use_case] = lambda: mock_create_room_use_case
    yield
    app.dependency_overrides = {}


def test_create_room_success(client, override_dependencies, mock_create_room_use_case, fake_room):
    payload = {
        "room": {
            "name": fake_room.name,
            "description": fake_room.description,
            "floor": fake_room.floor,
            "building_id": fake_room.building_id,
            "area": fake_room.area,
            "shape": fake_room.shape,
            "capacity": fake_room.capacity,
            "start_at": fake_room.start_at.isoformat(),
            "end_at": fake_room.end_at.isoformat(),
        }
    }

    response = client.post("/api/v1/room", json=payload)

    room_entity = Room(
        id=None,
        name=fake_room.name,
        description=fake_room.description,
        floor=fake_room.floor,
        building_id=fake_room.building_id,
        area=fake_room.area,
        shape=fake_room.shape,
        capacity=fake_room.capacity,
        start_at=fake_room.start_at,
        end_at=fake_room.end_at,
        created_at=None,
        updated_at=None,
    )
    mock_create_room_use_case.execute.assert_called_once_with(room_entity)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_room.id
    assert data["name"] == fake_room.name
    assert data["description"] == fake_room.description
    assert data["building_id"] == fake_room.building_id


def test_create_room_failed_creation_error(client, override_dependencies, mock_create_room_use_case, fake_room):
    mock_create_room_use_case.execute.side_effect = CreationFailedError("Room")

    payload = {
        "room": {
            "name": fake_room.name,
            "description": fake_room.description,
            "floor": fake_room.floor,
            "building_id": fake_room.building_id,
            "area": fake_room.area,
            "shape": fake_room.shape,
            "capacity": fake_room.capacity,
            "start_at": fake_room.start_at.isoformat(),
            "end_at": fake_room.end_at.isoformat(),
        }
    }

    response = client.post("/api/v1/room", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["detail"] == "Failed to create Room"


def test_end():
    print("\n\nEnd => Create Room route\n")
