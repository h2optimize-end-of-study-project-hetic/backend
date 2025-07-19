import pytest
from unittest.mock import Mock

from app.src.presentation.main import app
from app.src.presentation.dependencies import delete_tag_use_case
from app.src.use_cases.tag.delete_tag_use_case import DeleteTagUseCase
from app.src.common.exception import NotFoundError, DeletionFailedError, ForeignKeyConstraintError


@pytest.fixture
def mock_delete_tag_use_case():
    mock = Mock(spec=DeleteTagUseCase)
    mock.execute.return_value = True
    return mock


@pytest.fixture
def override_dependencies(mock_delete_tag_use_case):
    app.dependency_overrides[delete_tag_use_case] = lambda: mock_delete_tag_use_case
    yield
    app.dependency_overrides = {}


def test_delete_tag_success(client, override_dependencies, mock_delete_tag_use_case):
    tag_id = 1

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


def test_delete_tag_failed_tag_conected_to_other_entities(client, override_dependencies, mock_delete_tag_use_case):
    tag_id = 1
    mock_delete_tag_use_case.execute.side_effect = ForeignKeyConstraintError("Tag", "link width room", "room")

    response = client.delete(f"/api/v1/tag/{tag_id}")

    mock_delete_tag_use_case.execute.assert_called_once_with(tag_id)
    assert response.status_code == 406
    assert response.json()["detail"] == "Failed to execute request on Tag"


def test_delete_tag_failed_error(client, override_dependencies, mock_delete_tag_use_case):
    tag_id = 1
    mock_delete_tag_use_case.execute.side_effect = DeletionFailedError("Tag")

    response = client.delete(f"/api/v1/tag/{tag_id}")

    mock_delete_tag_use_case.execute.assert_called_once_with(tag_id)
    assert response.status_code == 406
    assert response.json()["detail"] == "Failed to delete Tag"


def test_delete_tag_failed_unexpectedly(client, override_dependencies, mock_delete_tag_use_case):
    tag_id = 1
    mock_delete_tag_use_case.execute.side_effect = Exception("Unexpectedly")

    response = client.delete(f"/api/v1/tag/{tag_id}")

    mock_delete_tag_use_case.execute.assert_called_once_with(tag_id)
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"


@pytest.mark.parametrize("tag_id", [-1, 0, "abc"])
def test_delete_tag_failed_invalid_tag_id(client, override_dependencies, mock_delete_tag_use_case, tag_id):
    response = client.get(f"/api/v1/tag/{tag_id}")

    assert response.status_code == 422
    mock_delete_tag_use_case.execute.assert_not_called()


def test_end():
    print("\n\nEnd => Delete Tag route\n")
