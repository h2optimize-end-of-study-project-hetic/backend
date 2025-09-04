import pytest
from unittest.mock import Mock

from app.src.presentation.main import app
from app.src.presentation.dependencies import delete_room_use_case
from app.src.use_cases.room.delete_room_use_case import DeleteRoomUseCase
from app.src.common.exception import DeletionFailedError
from app.src.presentation.api.secure_ressources import get_current_user_from_token


@pytest.fixture
def mock_delete_room_use_case():
    mock = Mock(spec=DeleteRoomUseCase)
    mock.execute.return_value = True
    return mock


@pytest.fixture
def override_dependencies(mock_delete_room_use_case, authenticated_client):
    client, user = authenticated_client
    app.dependency_overrides[delete_room_use_case] = lambda: mock_delete_room_use_case
    app.dependency_overrides[get_current_user_from_token] = lambda: user
    yield client, user
    app.dependency_overrides.clear()


def test_delete_room_success(override_dependencies, mock_delete_room_use_case):
    client, _ = override_dependencies
    room_id = 1

    response = client.delete(f"/api/v1/room/{room_id}")

    mock_delete_room_use_case.execute.assert_called_once_with(room_id)
    assert response.status_code == 204
    assert response.content == b""


def test_delete_room_failed_error(override_dependencies, mock_delete_room_use_case):
    client, _ = override_dependencies
    room_id = 1
    mock_delete_room_use_case.execute.side_effect = DeletionFailedError("Room")

    response = client.delete(f"/api/v1/room/{room_id}")

    mock_delete_room_use_case.execute.assert_called_once_with(room_id)
    assert response.status_code == 406
    assert response.json()["detail"] == "Failed to delete Room"


def test_end():
    print("\n\nEnd => Delete Room route\n")
