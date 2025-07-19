import pytest
from unittest.mock import MagicMock

from app.src.presentation.dependencies import (
    tag_repository,
    get_tag_by_id_use_case,
    get_tag_list_use_case,
    create_tag_use_case,
    update_tag_use_case,
    delete_tag_use_case,
)
from app.src.use_cases.tag.create_tag_use_case import CreateTagUseCase
from app.src.use_cases.tag.delete_tag_use_case import DeleteTagUseCase
from app.src.use_cases.tag.update_tag_use_case import UpdateTagUseCase
from app.src.use_cases.tag.get_tag_list_use_case import GetTagListUseCase
from app.src.use_cases.tag.get_tag_by_id_use_case import GetTagByIdUseCase
from app.src.infrastructure.db.repositories.tag_repository_sql import SQLTagRepository


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def mock_tag_repo(mock_session):
    return SQLTagRepository(mock_session)


def test_tag_repository_returns_sql_tag_repository(mock_session):
    repo = tag_repository(session=mock_session)
    assert isinstance(repo, SQLTagRepository)


def test_get_tag_by_id_use_case_returns_instance(mock_tag_repo):
    use_case = get_tag_by_id_use_case(tag_repository=mock_tag_repo)
    assert isinstance(use_case, GetTagByIdUseCase)


def test_get_tag_list_use_case_returns_instance(mock_tag_repo):
    use_case = get_tag_list_use_case(tag_repository=mock_tag_repo)
    assert isinstance(use_case, GetTagListUseCase)


def test_create_tag_use_case_returns_instance(mock_tag_repo):
    use_case = create_tag_use_case(tag_repository=mock_tag_repo)
    assert isinstance(use_case, CreateTagUseCase)


def test_update_tag_use_case_returns_instance(mock_tag_repo):
    use_case = update_tag_use_case(tag_repository=mock_tag_repo)
    assert isinstance(use_case, UpdateTagUseCase)


def test_delete_tag_use_case_returns_instance(mock_tag_repo):
    use_case = delete_tag_use_case(tag_repository=mock_tag_repo)
    assert isinstance(use_case, DeleteTagUseCase)


def test_end():
    print("\n\nEnd => dependencies module\n")
