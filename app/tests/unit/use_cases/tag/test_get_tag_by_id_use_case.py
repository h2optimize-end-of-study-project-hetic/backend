import pytest
from unittest.mock import Mock

from app.src.use_cases.tag.get_tag_by_id_use_case import GetTagByIdUseCase
from app.src.domain.interface_repositories.tag_repository import TagRepository


@pytest.fixture
def mock_tag_repo():
    return Mock(spec=TagRepository)


@pytest.fixture
def use_case(mock_tag_repo):
    return GetTagByIdUseCase(tag_repository=mock_tag_repo)


def test_get_tag_by_id_use_case_build(use_case, mock_tag_repo):
    assert use_case is not None
    assert use_case.tag_repository == mock_tag_repo


def test_get_tag_by_id_use_case_execute_success(use_case, mock_tag_repo, sample_tags_factory):
    fake_tag = sample_tags_factory(1, 2)[0]
    tag_id = 1

    mock_tag_repo.select_tag_by_id.return_value = fake_tag

    result = use_case.execute(tag_id, with_rooms=False)

    mock_tag_repo.select_tag_by_id.assert_called_once_with(tag_id, with_rooms=False)

    assert result == fake_tag


def test_end():
    print("\n\nEnd => Get Tag by ID usecase\n")
