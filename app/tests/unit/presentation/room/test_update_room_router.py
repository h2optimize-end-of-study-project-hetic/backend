import pytest
from unittest.mock import Mock

from app.src.presentation.main import app
from app.src.presentation.dependencies import update_tag_use_case
from app.src.use_cases.tag.update_tag_use_case import UpdateTagUseCase


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


def test_update_tag_success(authenticated_client, override_dependencies, mock_update_tag_use_case, fake_tag):
    client, _ = authenticated_client
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


def test_update_tag_failed_unexpectedly(authenticated_client, override_dependencies, mock_update_tag_use_case, fake_tag):
    client, _ = authenticated_client
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


def test_end():
    print("\n\nEnd => Update Tag route\n")
