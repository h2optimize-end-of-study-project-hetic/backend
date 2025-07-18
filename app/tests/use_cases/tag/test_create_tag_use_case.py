import pytest

from unittest.mock import Mock

from app.src.domain.entities.tag import Tag
from app.src.use_cases.tag.create_tag_use_case import CreateTagUseCase
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.domain.interface_repositories.room_repository import RoomRepository


@pytest.fixture
def mock_tag_repo():
    return Mock(spec=TagRepository)


@pytest.fixture
def mock_room_repo():
    return Mock(spec=RoomRepository)


@pytest.fixture
def use_case(mock_tag_repo, mock_room_repo):
    return CreateTagUseCase(tag_repository=mock_tag_repo, room_repository=mock_room_repo)


def test_create_tag_use_case_build(use_case, mock_tag_repo, mock_room_repo):
    assert use_case is not None
    assert use_case.tag_repository == mock_tag_repo
    assert use_case.room_repository == mock_room_repo


def test_create_tag_use_case_execute_success(use_case, mock_tag_repo, sample_tags_factory):
    fake_tag = sample_tags_factory(1, 2)[0]
    mock_tag_repo.create_tag.return_value = fake_tag

    result = use_case.execute(fake_tag)

    mock_tag_repo.create_tag.assert_called_once_with(fake_tag)
    assert result == fake_tag


def test_end():
    print("\n\nEnd => Create Tag usecase\n")
