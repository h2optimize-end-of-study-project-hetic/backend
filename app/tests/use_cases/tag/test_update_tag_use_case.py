import pytest

from unittest.mock import Mock

from app.src.domain.entities.tag import Tag
from app.src.use_cases.tag.update_tag_use_case import UpdateTagUseCase
from app.src.domain.interface_repositories.tag_repository import TagRepository


@pytest.fixture
def mock_tag_repo():
    return Mock(spec=TagRepository)


@pytest.fixture
def use_case(mock_tag_repo):
    return UpdateTagUseCase(tag_repository=mock_tag_repo)


@pytest.fixture
def fake_tag():
    return Tag(
        id=1,
        name="original name",
        description="original description",
        source_address="source",
        created_at="2025-07-17T20:14:19.947Z",
        updated_at="2025-07-17T20:14:19.947Z",
    )


def test_update_tag_use_case_start():
    print("\n\n- Update Tag usecase")


def test_update_tag_use_case_build(use_case, mock_tag_repo):
    assert use_case is not None
    assert use_case.tag_repository == mock_tag_repo


def test_update_tag_use_case_execute_success(use_case, mock_tag_repo, fake_tag):
    tag_id = 1
    tag_data = {"name": "updated name", "description": "updated description"}

    updated_tag = Tag(
        id=1,
        name="updated name",
        description="updated description",
        source_address="source",
        created_at=fake_tag.created_at,
        updated_at="2025-07-18T12:00:00.000Z",
    )

    mock_tag_repo.update_tag.return_value = updated_tag

    result = use_case.execute(tag_id, tag_data)

    mock_tag_repo.update_tag.assert_called_once_with(tag_id, tag_data)
    assert result == updated_tag
