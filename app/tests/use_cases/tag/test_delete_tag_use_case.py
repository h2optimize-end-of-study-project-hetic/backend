import pytest

from unittest.mock import Mock

from app.src.use_cases.tag.delete_tag_use_case import DeleteTagUseCase
from app.src.domain.interface_repositories.tag_repository import TagRepository


@pytest.fixture
def mock_tag_repo():
    return Mock(spec=TagRepository)


@pytest.fixture
def use_case(mock_tag_repo):
    return DeleteTagUseCase(tag_repository=mock_tag_repo)


def test_delete_tag_use_case_build(use_case, mock_tag_repo):
    assert use_case is not None
    assert use_case.tag_repository == mock_tag_repo


def test_delete_tag_use_case_execute_success(use_case, mock_tag_repo):
    tag_id = 56
    mock_tag_repo.delete_tag.return_value = True

    result = use_case.execute(tag_id)

    mock_tag_repo.delete_tag.assert_called_once_with(tag_id)
    assert result is True


def test_delete_tag_use_case_execute_failure(use_case, mock_tag_repo):
    tag_id = 72
    mock_tag_repo.delete_tag.return_value = False

    result = use_case.execute(tag_id)

    mock_tag_repo.delete_tag.assert_called_once_with(tag_id)
    assert result is False


def test_end():
    print("\n\nEnd => Delete Tag usecase\n")
