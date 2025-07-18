import pytest
from unittest.mock import Mock

from app.src.domain.entities.tag import Tag
from app.src.use_cases.tag.get_tag_by_id_use_case import GetTagByIdUseCase
from app.src.domain.interface_repositories.tag_repository import TagRepository


@pytest.fixture
def mock_tag_repo():
    return Mock(spec=TagRepository)


@pytest.fixture
def use_case(mock_tag_repo):
    return GetTagByIdUseCase(tag_repository=mock_tag_repo)


@pytest.fixture
def fake_tag():
    return Tag(
        id=1,
        name="Test Tag",
        description="desc",
        source_address="source_addr",
        created_at="2025-07-17T20:14:19.947Z",
        updated_at="2025-07-17T20:14:19.947Z",
    )


def test_get_tag_by_id_use_case_start():
    print("\n\n- Get Tag by ID usecase")


def test_get_tag_by_id_use_case_build(use_case, mock_tag_repo):
    assert use_case is not None
    assert use_case.tag_repository == mock_tag_repo


def test_get_tag_by_id_use_case_execute_success(use_case, mock_tag_repo, fake_tag):
    tag_id = 1

    mock_tag_repo.select_tag_by_id.return_value = fake_tag

    result = use_case.execute(tag_id)

    mock_tag_repo.select_tag_by_id.assert_called_once_with(tag_id)

    assert result == fake_tag
