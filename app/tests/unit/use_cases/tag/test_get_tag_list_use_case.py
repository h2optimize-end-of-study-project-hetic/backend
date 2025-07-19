import pytest

from unittest.mock import Mock

from app.src.common.exception import DecodedFailedError
from app.src.use_cases.tag.get_tag_list_use_case import GetTagListUseCase, PaginatedTag


@pytest.fixture
def mock_tag_repo():
    return Mock()


@pytest.fixture
def use_case(mock_tag_repo):
    return GetTagListUseCase(tag_repository=mock_tag_repo)


def test_get_tag_list_use_case_build(use_case, mock_tag_repo):
    assert use_case is not None
    assert use_case.tag_repository == mock_tag_repo


def test_get_tag_list_use_case_success_no_cursor(use_case, mock_tag_repo, sample_tags_factory):
    sample_tags = sample_tags_factory(1, 26)

    limit = 10
    total = 25
    first_tag = sample_tags[0]
    last_tag = sample_tags[-5]

    mock_tag_repo.paginate_tags.return_value = (sample_tags[:11], total, first_tag, last_tag)

    result: PaginatedTag = use_case.execute(cursor=None, limit=limit)

    assert result.total == 25
    assert result.chunk_size == 10
    assert result.chunk_count == 3
    assert result.current_cursor == "id=1"
    assert result.next_cursor == "id=11"
    assert result.first_cursor == "id=1"
    assert result.last_cursor == "id=21"
    assert isinstance(result.tags, list)
    assert result.tags == sample_tags[:10]
    assert len(result.tags) == 10

    mock_tag_repo.paginate_tags.assert_called_once_with(None, limit + 1)


def test_get_tag_list_use_case_success_with_cursor(use_case, mock_tag_repo, sample_tags_factory):
    sample_tags = sample_tags_factory(1, 26)

    limit = 10
    total = 25
    first_tag = sample_tags[0]
    last_tag = sample_tags[-5]

    mock_tag_repo.paginate_tags.return_value = (sample_tags[10:21], total, first_tag, last_tag)

    result: PaginatedTag = use_case.execute(cursor="id=11", limit=limit)

    assert result.total == 25
    assert result.chunk_size == 10
    assert result.chunk_count == 3
    assert result.current_cursor == "id=11"
    assert result.next_cursor == "id=21"
    assert result.first_cursor == "id=1"
    assert result.last_cursor == "id=21"
    assert isinstance(result.tags, list)
    assert result.tags == sample_tags[10:20]
    assert len(result.tags) == 10

    mock_tag_repo.paginate_tags.assert_called_once_with("11", limit + 1)


def test_get_tag_list_use_case_failed_with_invalid_cursor(use_case):
    with pytest.raises(DecodedFailedError, match="Failed to decode Tag"):
        use_case.execute(cursor="id11", limit=10)


def test_get_tag_list_use_case_success_with_no_limit(use_case, mock_tag_repo, sample_tags_factory):
    sample_tags = sample_tags_factory(1, 26)

    limit = 20
    total = 25
    first_tag = sample_tags[0]
    last_tag = sample_tags[-5]

    mock_tag_repo.paginate_tags.return_value = (sample_tags[:21], total, first_tag, last_tag)

    result: PaginatedTag = use_case.execute(cursor="id=1")

    assert result.total == 25
    assert result.chunk_size == 20
    assert result.chunk_count == 2
    assert result.current_cursor == "id=1"
    assert result.next_cursor == "id=21"
    assert result.first_cursor == "id=1"
    assert result.last_cursor == "id=21"
    assert isinstance(result.tags, list)
    assert result.tags == sample_tags[:20]
    assert len(result.tags) == 20

    mock_tag_repo.paginate_tags.assert_called_once_with("1", limit + 1)


def test_get_tag_list_use_case_success_with_cursor_last_cursor(use_case, mock_tag_repo, sample_tags_factory):
    sample_tags = sample_tags_factory(1, 26)

    limit = 10
    total = 25
    first_tag = sample_tags[0]
    last_tag = sample_tags[-5]

    mock_tag_repo.paginate_tags.return_value = (sample_tags[21:25], total, first_tag, last_tag)

    result: PaginatedTag = use_case.execute(cursor="id=21", limit=limit)

    assert result.total == 25
    assert result.chunk_size == 4
    assert result.chunk_count == 3
    assert result.current_cursor == "id=21"
    assert result.next_cursor is None
    assert result.first_cursor == "id=1"
    assert result.last_cursor == "id=21"
    assert isinstance(result.tags, list)
    assert result.tags == sample_tags[21:25]
    assert len(result.tags) == 4

    mock_tag_repo.paginate_tags.assert_called_once_with("21", limit + 1)


def test_get_tag_list_use_case_next_cursor(use_case, mock_tag_repo, sample_tags_factory):
    sample_tags = sample_tags_factory(1, 26)

    limit = 2
    total = 25
    first_tag = sample_tags[0]
    last_tag = sample_tags[-1]

    mock_tag_repo.paginate_tags.return_value = (sample_tags[:3], total, first_tag, last_tag)

    result: PaginatedTag = use_case.execute(cursor=None, limit=limit)

    assert result.total == 25
    assert result.chunk_size == 2
    assert result.chunk_count == 13
    assert result.current_cursor == "id=1"
    assert result.next_cursor == "id=3"
    assert result.first_cursor == "id=1"
    assert result.last_cursor == "id=25"
    assert isinstance(result.tags, list)
    assert result.tags == sample_tags[:2]
    assert len(result.tags) == 2


def test_end():
    print("\n\nEnd => Get Tag list usecase\n")
