import pytest
from unittest.mock import Mock
from app.src.presentation.main import app
from app.src.domain.entities.tag import Tag
from app.src.presentation.dependencies import create_tag_use_case
from app.src.use_cases.tag.create_tag_use_case import CreateTagUseCase
from app.src.common.exception import AlreadyExistsError, CreationFailedError
from app.src.presentation.api.secure_ressources import get_current_user_from_token
from app.src.domain.entities.user import User
from app.src.domain.entities.role import Role


@pytest.fixture
def fake_tag(sample_tags_factory):
    """Fournit un tag factice."""
    return sample_tags_factory(1, 2)[0]


@pytest.fixture
def fake_user(sample_users_factory):
    """Fournit un utilisateur admin factice pour les tests."""
    user = sample_users_factory(1, 2)[0]
    user.role = Role.admin.value
    user.is_active = True
    return user


@pytest.fixture
def mock_create_tag_use_case(fake_tag):
    mock = Mock(spec=CreateTagUseCase)
    mock.execute.return_value = fake_tag
    return mock


@pytest.fixture
def authenticated_client(client, fake_user):
    def mock_current_user():
        return fake_user

    app.dependency_overrides[get_current_user_from_token] = mock_current_user
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def override_dependencies(mock_create_tag_use_case):
    app.dependency_overrides[create_tag_use_case] = lambda: mock_create_tag_use_case
    yield
    app.dependency_overrides.clear()


def test_create_tag_success(authenticated_client, override_dependencies, mock_create_tag_use_case, fake_tag):
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }

    response = authenticated_client.post("/api/v1/tag", json=payload)

    tag_entity = Tag(
        id=None,
        name=fake_tag.name,
        description=fake_tag.description,
        source_address=fake_tag.source_address,
        created_at=None,
        updated_at=None,
    )

    mock_create_tag_use_case.execute.assert_called_once_with(tag_entity)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_tag.id
    assert data["name"] == fake_tag.name
    assert data["description"] == fake_tag.description
    assert data["source_address"] == fake_tag.source_address
    assert data["created_at"] == fake_tag.created_at.isoformat()
    assert data["updated_at"] == fake_tag.updated_at.isoformat()


@pytest.mark.parametrize(
    "payload",
    [
        {"tag": {"description": "desc", "source_address": "addr"}},  # no name
        {"tag": {"name": "te", "description": "desc", "source_address": "addr"}},  # name too short
        {"tag": {"name": "x"*256, "description": "desc", "source_address": "addr"}},  # name too long
        {"tag": {"name": "Valid", "description": "desc"}},  # no source_address
        {"tag": {"name": "Valid", "description": "desc", "source_address": "x"}},  # source_address too short
    ]
)
def test_create_tag_invalid_payload(authenticated_client, override_dependencies, mock_create_tag_use_case, payload):
    response = authenticated_client.post("/api/v1/tag", json=payload)
    mock_create_tag_use_case.execute.assert_not_called()
    assert response.status_code == 422


def test_create_tag_already_exists(authenticated_client, override_dependencies, mock_create_tag_use_case, fake_tag):
    mock_create_tag_use_case.execute.side_effect = AlreadyExistsError("Tag", "source_address", fake_tag.source_address)
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }
    response = authenticated_client.post("/api/v1/tag", json=payload)

    tag_entity = Tag(
        id=None,
        name=fake_tag.name,
        description=fake_tag.description,
        source_address=fake_tag.source_address,
        created_at=None,
        updated_at=None,
    )

    mock_create_tag_use_case.execute.assert_called_once_with(tag_entity)
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == f"Tag with source_address '{fake_tag.source_address}' already exists"


def test_create_tag_failed_creation(authenticated_client, override_dependencies, mock_create_tag_use_case, fake_tag):
    mock_create_tag_use_case.execute.side_effect = CreationFailedError("Tag")
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }
    response = authenticated_client.post("/api/v1/tag", json=payload)
    assert response.status_code == 406
    data = response.json()
    assert data["detail"] == "Failed to create Tag"


def test_create_tag_failed_unexpected_error(authenticated_client, override_dependencies, mock_create_tag_use_case, fake_tag):
    mock_create_tag_use_case.execute.side_effect = Exception("Unexpectedly")
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }
    response = authenticated_client.post("/api/v1/tag", json=payload)

    tag_entity = Tag(
        id=None,
        name=fake_tag.name,
        description=fake_tag.description,
        source_address=fake_tag.source_address,
        created_at=None,
        updated_at=None,
    )

    mock_create_tag_use_case.execute.assert_called_once_with(tag_entity)
    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Internal server error"


def test_create_tag_unauthorized(client, fake_tag):
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }
    response = client.post("/api/v1/tag", json=payload)
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_end():
    print("\n\nEnd => Create Tag route\n")
