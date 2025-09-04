import pytest
from unittest.mock import Mock
from app.src.presentation.main import app
from app.src.domain.entities.tag import Tag
from app.src.domain.entities.user import User
from app.src.domain.entities.role import Role
from app.src.presentation.dependencies import delete_tag_use_case
from app.src.presentation.api.secure_ressources import get_current_user_from_token
from app.src.use_cases.tag.delete_tag_use_case import DeleteTagUseCase
from app.src.common.exception import NotFoundError, DeletionFailedError, ForeignKeyConstraintError


@pytest.fixture
def fake_tag(sample_tags_factory):
    return sample_tags_factory(1, 2)[0]


@pytest.fixture
def fake_user(sample_users_factory):
    users = sample_users_factory(1, 2)
    user = users[0]
    user.role = Role.staff.value
    return user


@pytest.fixture
def mock_delete_tag_use_case():
    mock = Mock(spec=DeleteTagUseCase)
    mock.execute.return_value = True
    return mock


@pytest.fixture
def mock_current_user(fake_user):
    def _mock():
        return fake_user
    return _mock


@pytest.fixture
def override_dependencies(mock_delete_tag_use_case, mock_current_user):
    app.dependency_overrides[delete_tag_use_case] = lambda: mock_delete_tag_use_case
    app.dependency_overrides[get_current_user_from_token] = mock_current_user
    yield
    app.dependency_overrides = {}


def test_delete_tag_success(client, override_dependencies, mock_delete_tag_use_case, fake_tag):
    tag_id = fake_tag.id
    
    response = client.delete(f"/api/v1/tag/{tag_id}")
    
    mock_delete_tag_use_case.execute.assert_called_once_with(tag_id)
    assert response.status_code == 204
    assert response.content == b""


def test_delete_tag_failed_tag_not_found(client, override_dependencies, mock_delete_tag_use_case):
    tag_id = 999
    mock_delete_tag_use_case.execute.side_effect = NotFoundError("Tag", tag_id)
    
    response = client.delete(f"/api/v1/tag/{tag_id}")
    
    mock_delete_tag_use_case.execute.assert_called_once_with(tag_id)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Tag with ID '{tag_id}' not found"


def test_delete_tag_failed_tag_connected_to_other_entities(client, override_dependencies, mock_delete_tag_use_case, fake_tag):
    tag_id = fake_tag.id
    mock_delete_tag_use_case.execute.side_effect = ForeignKeyConstraintError("Tag", "link width room", "room")
    
    response = client.delete(f"/api/v1/tag/{tag_id}")
    
    mock_delete_tag_use_case.execute.assert_called_once_with(tag_id)
    assert response.status_code == 406
    assert response.json()["detail"] == "Failed to execute request on Tag"


def test_delete_tag_failed_error(client, override_dependencies, mock_delete_tag_use_case, fake_tag):
    tag_id = fake_tag.id
    mock_delete_tag_use_case.execute.side_effect = DeletionFailedError("Tag")
    
    response = client.delete(f"/api/v1/tag/{tag_id}")
    
    mock_delete_tag_use_case.execute.assert_called_once_with(tag_id)
    assert response.status_code == 406
    assert response.json()["detail"] == "Failed to delete Tag"


def test_delete_tag_failed_unexpectedly(client, override_dependencies, mock_delete_tag_use_case, fake_tag):
    tag_id = fake_tag.id
    mock_delete_tag_use_case.execute.side_effect = Exception("Unexpectedly")
    
    response = client.delete(f"/api/v1/tag/{tag_id}")
    
    mock_delete_tag_use_case.execute.assert_called_once_with(tag_id)
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"


@pytest.mark.parametrize("tag_id", [-1, 0, "abc"])
def test_delete_tag_failed_invalid_tag_id(client, override_dependencies, mock_delete_tag_use_case, tag_id):
    response = client.delete(f"/api/v1/tag/{tag_id}")
    
    assert response.status_code == 422
    mock_delete_tag_use_case.execute.assert_not_called()


def test_delete_tag_unauthorized_without_token(client):
    tag_id = 1
    
    response = client.delete(f"/api/v1/tag/{tag_id}")
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_delete_tag_insufficient_permissions(client, mock_delete_tag_use_case, fake_user):
    fake_user.role = Role.guest.value
    tag_id = 1
    
    def mock_current_user_insufficient():
        return fake_user
    
    app.dependency_overrides[delete_tag_use_case] = lambda: mock_delete_tag_use_case
    app.dependency_overrides[get_current_user_from_token] = mock_current_user_insufficient
    
    response = client.delete(f"/api/v1/tag/{tag_id}")
    
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Insufficient permissions"
    
    app.dependency_overrides = {}


def test_end():
    print("\n\nEnd => Delete Tag route\n")