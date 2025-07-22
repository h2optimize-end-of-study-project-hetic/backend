import pytest
from unittest.mock import Mock

from app.src.presentation.main import app
from app.src.presentation.dependencies import update_tag_use_case
from app.src.use_cases.tag.update_tag_use_case import UpdateTagUseCase
from app.src.common.exception import NotFoundError, AlreadyExistsError, UpdateFailedError


@pytest.fixture
def fake_tag(sample_tags_factory):
    return sample_tags_factory(1, 2)[0]


@pytest.fixture
def mock_update_tag_use_case(fake_tag):
    mock = Mock(spec=UpdateTagUseCase)
    mock.execute.return_value = fake_tag
    return mock


@pytest.fixture
def override_dependencies(mock_update_tag_use_case):
    app.dependency_overrides[update_tag_use_case] = lambda: mock_update_tag_use_case
    yield
    app.dependency_overrides = {}


def test_update_tag_success(client, override_dependencies, mock_update_tag_use_case, fake_tag):
    fake_tag.name = "Updated name"
    fake_tag.description = "Updated description"
    fake_tag.source_address = "Updated src address"
    mock_update_tag_use_case.execute.return_value = fake_tag

    payload = {
        "tag": {
            "name": "Updated name",
            "description": "Updated description",
            "source_address": "Updated src address",
        }
    }
    tag_id = fake_tag.id

    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)

    mock_update_tag_use_case.execute.assert_called_once_with(tag_id, payload["tag"])
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == fake_tag.id
    assert data["name"] == fake_tag.name
    assert data["description"] == fake_tag.description
    assert data["source_address"] == fake_tag.source_address
    assert data["created_at"] == fake_tag.created_at.isoformat()
    assert data["updated_at"] == fake_tag.updated_at.isoformat()


@pytest.mark.parametrize("tag_id", [-1, 0, "abc"])
def test_update_tag_failed_invalid_tag_id(client, override_dependencies, mock_update_tag_use_case, tag_id):
    payload = {
        "tag": {
            "name": "Updated name",
            "description": "Updated description",
            "source_address": "Updated src address",
        }
    }
    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)

    assert response.status_code == 422
    mock_update_tag_use_case.execute.assert_not_called()


def test_update_tag_failed_tag_not_found(client, override_dependencies, mock_update_tag_use_case):
    tag_id = 999
    mock_update_tag_use_case.execute.side_effect = NotFoundError("Tag", tag_id)

    payload = {
        "tag": {
            "name": "Updated name",
            "description": "Updated description",
            "source_address": "Updated src address",
        }
    }
    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)
    mock_update_tag_use_case.execute.assert_called_once_with(tag_id, payload["tag"])
    assert response.status_code == 404
    assert response.json()["detail"] == f"Tag with ID '{tag_id}' not found"


def test_update_tag_failed_already_exists(client, override_dependencies, mock_update_tag_use_case, fake_tag):
    mock_update_tag_use_case.execute.side_effect = AlreadyExistsError("Tag", "source_address", "existing_address")

    tag_id = fake_tag.id
    payload = {
        "tag": {
            "name": "Updated name",
            "description": "Updated description",
            "source_address": "existing_address",
        }
    }

    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)

    mock_update_tag_use_case.execute.assert_called_once_with(tag_id, payload["tag"])
    assert response.status_code == 409
    assert response.json()["detail"] == "Tag with source_address 'existing_address' already exists"


def test_update_tag_failed(client, override_dependencies, mock_update_tag_use_case, fake_tag):
    tag_id = fake_tag.id
    payload = {"tag": {"name": "Updated name"}}
    mock_update_tag_use_case.execute.side_effect = UpdateFailedError("Tag")

    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)

    mock_update_tag_use_case.execute.assert_called_once_with(tag_id, payload["tag"])
    assert response.status_code == 406
    assert response.json()["detail"] == "Failed to update Tag"


def test_update_tag_failed_unexpectedly(client, override_dependencies, mock_update_tag_use_case, fake_tag):
    tag_id = fake_tag.id
    payload = {
        "tag": {
            "name": "Updated name",
            "description": "Updated description",
            "source_address": "Updated src address",
        }
    }
    mock_update_tag_use_case.execute.side_effect = Exception("unexpectedly")

    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)

    mock_update_tag_use_case.execute.assert_called_once_with(tag_id, payload["tag"])
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"


@pytest.mark.parametrize(
    "name",
    [
        "te",
        "",
        "Lorem ipsum dolor, sit amet consectetur adipisicing elit. Quod quo harum officia alias reiciendis tenetur placeat autem dolore repellendus distinctio.Lorem ipsum dolor, sit amet consectetur adipisicing elit. Quod quo harum officia alias reiciendis tenetur placeat autem dolore repellendus distinctio.",
    ],
)
def test_update_tag_failed_invalid_name(client, override_dependencies, mock_update_tag_use_case, name, fake_tag):
    payload = {
        "tag": {
            "name": name,
            "description": "Updated description",
            "source_address": "Updated src address",
        }
    }
    response = client.patch(f"/api/v1/tag/{fake_tag.id}", json=payload)

    assert response.status_code == 422
    mock_update_tag_use_case.execute.assert_not_called()


@pytest.mark.parametrize("source_address", ["te", ""])
def test_update_tag_failed_invalid_source_address(
    client, override_dependencies, mock_update_tag_use_case, source_address, fake_tag
):
    payload = {
        "tag": {
            "name": "Updated name",
            "description": "Updated description",
            "source_address": source_address,
        }
    }
    response = client.patch(f"/api/v1/tag/{fake_tag.id}", json=payload)

    assert response.status_code == 422
    mock_update_tag_use_case.execute.assert_not_called()


def test_update_tag_success_no_name(client, override_dependencies, mock_update_tag_use_case, fake_tag):
    fake_tag.description = "Updated description"
    fake_tag.source_address = "Updated src address"
    mock_update_tag_use_case.execute.return_value = fake_tag

    payload = {
        "tag": {
            "description": "Updated description",
            "source_address": "Updated src address",
        }
    }
    tag_id = fake_tag.id

    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)

    mock_update_tag_use_case.execute.assert_called_once_with(tag_id, payload["tag"])
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == fake_tag.id
    assert data["name"] == fake_tag.name
    assert data["description"] == fake_tag.description
    assert data["source_address"] == fake_tag.source_address
    assert data["created_at"] == fake_tag.created_at.isoformat()
    assert data["updated_at"] == fake_tag.updated_at.isoformat()


def test_update_tag_success_no_description(client, override_dependencies, mock_update_tag_use_case, fake_tag):
    fake_tag.name = "Updated name"
    fake_tag.source_address = "Updated src address"
    mock_update_tag_use_case.execute.return_value = fake_tag

    payload = {
        "tag": {
            "name": "Updated name",
            "source_address": "Updated src address",
        }
    }
    tag_id = fake_tag.id

    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)

    mock_update_tag_use_case.execute.assert_called_once_with(tag_id, payload["tag"])
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == fake_tag.id
    assert data["name"] == fake_tag.name
    assert data["description"] == fake_tag.description
    assert data["source_address"] == fake_tag.source_address
    assert data["created_at"] == fake_tag.created_at.isoformat()
    assert data["updated_at"] == fake_tag.updated_at.isoformat()


def test_update_tag_success_no_source_address(client, override_dependencies, mock_update_tag_use_case, fake_tag):
    fake_tag.name = "Updated name"
    fake_tag.description = "Updated description"
    mock_update_tag_use_case.execute.return_value = fake_tag

    payload = {
        "tag": {
            "name": "Updated name",
            "description": "Updated description",
        }
    }
    tag_id = fake_tag.id

    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)

    mock_update_tag_use_case.execute.assert_called_once_with(tag_id, payload["tag"])
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == fake_tag.id
    assert data["name"] == fake_tag.name
    assert data["description"] == fake_tag.description
    assert data["source_address"] == fake_tag.source_address
    assert data["created_at"] == fake_tag.created_at.isoformat()
    assert data["updated_at"] == fake_tag.updated_at.isoformat()


def test_end():
    print("\n\nEnd => Update Tag route\n")

