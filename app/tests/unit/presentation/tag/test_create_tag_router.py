import pytest
from unittest.mock import Mock

from app.src.presentation.main import app
from app.src.domain.entities.tag import Tag
from app.src.presentation.dependencies import create_tag_use_case
from app.src.use_cases.tag.create_tag_use_case import CreateTagUseCase
from app.src.common.exception import AlreadyExistsError, CreationFailedError


@pytest.fixture
def fake_tag(sample_tags_factory):
    return sample_tags_factory(1, 2)[0]


@pytest.fixture
def mock_create_tag_use_case(fake_tag):
    mock = Mock(spec=CreateTagUseCase)
    mock.execute.return_value = fake_tag
    return mock


@pytest.fixture
def override_dependencies(mock_create_tag_use_case):
    app.dependency_overrides[create_tag_use_case] = lambda: mock_create_tag_use_case
    yield
    app.dependency_overrides = {}


def test_create_tag_success(client, override_dependencies, mock_create_tag_use_case, fake_tag):
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }

    response = client.post("/api/v1/tag", json=payload)
    tag = Tag(
        id=None,
        name=fake_tag.name,
        description=fake_tag.description,
        source_address=fake_tag.source_address,
        created_at=None,
        updated_at=None,
    )
    mock_create_tag_use_case.execute.assert_called_once_with(tag)
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == fake_tag.id
    assert data["name"] == fake_tag.name
    assert data["description"] == fake_tag.description
    assert data["source_address"] == fake_tag.source_address
    assert data["created_at"] == fake_tag.created_at.isoformat()
    assert data["updated_at"] == fake_tag.updated_at.isoformat()


def test_create_tag_failed_no_name(client, override_dependencies, mock_create_tag_use_case, fake_tag):
    payload = {
        "tag": {
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }
    response = client.post("/api/v1/tag", json=payload)
    mock_create_tag_use_case.execute.assert_not_called()
    assert response.status_code == 422


def test_create_tag_failed_invalid_name_to_short(client, override_dependencies, mock_create_tag_use_case, fake_tag):
    payload = {
        "tag": {
            "name": "te",
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }
    response = client.post("/api/v1/tag", json=payload)
    mock_create_tag_use_case.execute.assert_not_called()
    assert response.status_code == 422


def test_create_tag_failed_invalid_name_to_long(client, override_dependencies, mock_create_tag_use_case, fake_tag):
    payload = {
        "tag": {
            "name": "Lorem ipsum dolor, sit amet consectetur adipisicing elit. Quod quo harum officia alias reiciendis tenetur placeat autem dolore repellendus distinctio.Lorem ipsum dolor, sit amet consectetur adipisicing elit. Quod quo harum officia alias reiciendis tenetur placeat autem dolore repellendus distinctio.",
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }
    response = client.post("/api/v1/tag", json=payload)
    mock_create_tag_use_case.execute.assert_not_called()
    assert response.status_code == 422


def test_create_tag_success_no_description(client, override_dependencies, mock_create_tag_use_case, fake_tag):
    mock_create_tag_use_case.execute.return_value = Tag(
        id=fake_tag.id,
        name=fake_tag.name,
        description=None,
        source_address=fake_tag.source_address,
        created_at=fake_tag.created_at,
        updated_at=fake_tag.updated_at,
    )

    payload = {"tag": {"name": fake_tag.name, "source_address": fake_tag.source_address}}

    response = client.post("/api/v1/tag", json=payload)
    tag = Tag(
        id=None,
        name=fake_tag.name,
        description=None,
        source_address=fake_tag.source_address,
        created_at=None,
        updated_at=None,
    )
    mock_create_tag_use_case.execute.assert_called_once_with(tag)
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == fake_tag.id
    assert data["name"] == fake_tag.name
    assert data["description"] is None
    assert data["source_address"] == fake_tag.source_address
    assert data["created_at"] == fake_tag.created_at.isoformat()
    assert data["updated_at"] == fake_tag.updated_at.isoformat()


def test_create_tag_failed_no_source_address(client, override_dependencies, mock_create_tag_use_case, fake_tag):
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
        }
    }
    response = client.post("/api/v1/tag", json=payload)
    mock_create_tag_use_case.execute.assert_not_called()
    assert response.status_code == 422


def test_create_tag_failed_invalid_source_address_to_short(
    client, override_dependencies, mock_create_tag_use_case, fake_tag
):
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": "te",
        }
    }
    response = client.post("/api/v1/tag", json=payload)
    mock_create_tag_use_case.execute.assert_not_called()
    assert response.status_code == 422


def test_create_tag_failed_tag_already_exist(client, override_dependencies, mock_create_tag_use_case, fake_tag):
    mock_create_tag_use_case.execute.side_effect = AlreadyExistsError("Tag", "source_address", fake_tag.source_address)
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }
    response = client.post("/api/v1/tag", json=payload)
    tag = Tag(
        id=None,
        name=fake_tag.name,
        description=fake_tag.description,
        source_address=fake_tag.source_address,
        created_at=None,
        updated_at=None,
    )
    mock_create_tag_use_case.execute.assert_called_once_with(tag)
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == f"Tag with source_address '{fake_tag.source_address}' already exists"


def test_create_tag_failed_tag(client, override_dependencies, mock_create_tag_use_case, fake_tag):
    mock_create_tag_use_case.execute.side_effect = CreationFailedError("Tag")
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }
    response = client.post("/api/v1/tag", json=payload)
    assert response.status_code == 406
    data = response.json()
    assert data["detail"] == "Failed to create Tag"


def test_create_tag_failed_tag_failed_unexpectedly(client, override_dependencies, mock_create_tag_use_case, fake_tag):
    mock_create_tag_use_case.execute.side_effect = Exception("Unexpectedly")
    payload = {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }
    response = client.post("/api/v1/tag", json=payload)
    tag = Tag(
        id=None,
        name=fake_tag.name,
        description=fake_tag.description,
        source_address=fake_tag.source_address,
        created_at=None,
        updated_at=None,
    )
    mock_create_tag_use_case.execute.assert_called_once_with(tag)
    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Internal server error"


def test_end():
    print("\n\nEnd => Create Tag route\n")
