import pytest
from unittest.mock import Mock
from app.src.presentation.main import app
from app.src.domain.entities.room import Room
from app.src.domain.entities.user import User
from app.src.domain.entities.role import Role
from app.src.presentation.dependencies import create_room_use_case
from app.src.presentation.api.secure_ressources import get_current_user_from_token
from app.src.use_cases.room.create_room_use_case import CreateRoomUseCase
from app.src.common.exception import CreationFailedError


@pytest.fixture
def fake_room(sample_rooms_factory):
    return sample_rooms_factory(1, 2)[0]


@pytest.fixture
def fake_user(sample_users_factory):
    users = sample_users_factory(1, 2)
    user = users[0]
    user.role = Role.staff.value
    return user


@pytest.fixture
def mock_create_room_use_case(fake_room):
    mock = Mock(spec=CreateRoomUseCase)
    mock.execute.return_value = fake_room
    return mock


@pytest.fixture
def mock_current_user(fake_user):
    def _mock():
        return fake_user
    return _mock


@pytest.fixture
def override_dependencies(mock_create_room_use_case, mock_current_user):
    app.dependency_overrides[create_room_use_case] = lambda: mock_create_room_use_case
    app.dependency_overrides[get_current_user_from_token] = mock_current_user
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


def test_create_room_unauthorized_without_token(client):
    payload = {
        "room": {
            "name": "Test Room",
            "description": "Test Description",
            "floor": 1,
            "building_id": 1,
            "area": 25.5,
            "shape": [[0, 0], [10, 10]],
            "capacity": 10,
        }
    }

    response = client.post("/api/v1/room", json=payload)
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_create_room_insufficient_permissions(client, mock_create_room_use_case, fake_user):
    fake_user.role = Role.guest.value
    
    def mock_current_user_insufficient():
        return fake_user
    
    app.dependency_overrides[create_room_use_case] = lambda: mock_create_room_use_case
    app.dependency_overrides[get_current_user_from_token] = mock_current_user_insufficient
    
    payload = {
        "room": {
            "name": "Test Room",
            "description": "Test Description",
            "floor": 1,
            "building_id": 1,
            "area": 25.5,
            "shape": [[0, 0], [10, 10]],
            "capacity": 10,
        }
    }

    response = client.post("/api/v1/room", json=payload)
    
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Insufficient permissions"
    
    app.dependency_overrides = {}


def test_end():
    print("\n\nEnd => Create Room route\n")