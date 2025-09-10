import pytest
from unittest.mock import Mock

from app.src.presentation.main import app
from app.src.common.exception import NotFoundError
from app.src.presentation.dependencies import get_tag_by_id_use_case
from app.src.use_cases.tag.get_tag_by_id_use_case import GetTagByIdUseCase


@pytest.fixture
def fake_tag(sample_tags_factory):
    return sample_tags_factory(1, 2)[0]


@pytest.fixture
def mock_get_tag_by_id_use_case(fake_tag):
    mock = Mock(spec=GetTagByIdUseCase)
    mock.execute.return_value = fake_tag
    return mock


@pytest.fixture
def override_dependencies(mock_get_tag_by_id_use_case):
    app.dependency_overrides[get_tag_by_id_use_case] = lambda: mock_get_tag_by_id_use_case
    yield
    app.dependency_overrides.clear()


def test_get_tag_by_id_success(authenticated_client, override_dependencies, mock_get_tag_by_id_use_case, fake_tag):
    client, user = authenticated_client
    tag_id = fake_tag.id

    response = client.get(f"/api/v1/tag/{tag_id}")

    mock_get_tag_by_id_use_case.execute.assert_called_once_with(tag_id, with_rooms=False)
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == fake_tag.id
    assert data["name"] == fake_tag.name
    assert data["description"] == fake_tag.description
    assert data["source_address"] == fake_tag.source_address
    assert data["created_at"] == fake_tag.created_at.isoformat()
    assert data["updated_at"] == fake_tag.updated_at.isoformat()


@pytest.mark.parametrize("tag_id", [-1, 0, "abc"])
def test_get_tag_by_id_invalid_id(authenticated_client, override_dependencies, mock_get_tag_by_id_use_case, tag_id):
    client, _ = authenticated_client
    response = client.get(f"/api/v1/tag/{tag_id}")

    assert response.status_code == 422
    mock_get_tag_by_id_use_case.execute.assert_not_called()


def test_get_tag_by_id_not_found(authenticated_client, override_dependencies, mock_get_tag_by_id_use_case):
    client, _ = authenticated_client
    tag_id = 999
    mock_get_tag_by_id_use_case.execute.side_effect = NotFoundError("Tag", tag_id)

    response = client.get(f"/api/v1/tag/{tag_id}")

    mock_get_tag_by_id_use_case.execute.assert_called_once_with(tag_id, with_rooms=False)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Tag with ID '{tag_id}' not found"


def test_get_tag_by_id_unexpected_error(authenticated_client, override_dependencies, mock_get_tag_by_id_use_case):
    client, _ = authenticated_client
    tag_id = 1
    mock_get_tag_by_id_use_case.execute.side_effect = Exception("Unexpectedly")

    response = client.get(f"/api/v1/tag/{tag_id}")

    mock_get_tag_by_id_use_case.execute.assert_called_once_with(tag_id, with_rooms=False)
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"


def test_get_tag_by_id_unauthorized(client, override_dependencies):
    tag_id = 1
    response = client.get(f"/api/v1/tag/{tag_id}")

    assert response.status_code == 401
    assert "detail" in response.json()


def test_end():
    print("\n\nEnd => Get Tag by ID route\n")
