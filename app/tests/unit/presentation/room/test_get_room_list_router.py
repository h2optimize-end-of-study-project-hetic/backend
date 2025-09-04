import pytest
from unittest.mock import Mock

from app.src.presentation.main import app
from app.src.presentation.dependencies import get_tag_list_use_case
from app.src.use_cases.tag.get_tag_list_use_case import GetTagListUseCase


@pytest.fixture
def fake_tags(sample_tags_factory):
    return sample_tags_factory(1, 26)


@pytest.fixture
def mock_get_tag_list_use_case(fake_tags):
    mock = Mock(spec=GetTagListUseCase)
    mock.execute.return_value = Mock(
        tags=fake_tags[:10],
        total=25,
        chunk_size=10,
        chunk_count=3,
        current_cursor="id=1",
        first_cursor="id=1",
        last_cursor="id=21",
        next_cursor="id=11",
    )
    return mock


@pytest.fixture
def override_dependencies(mock_get_tag_list_use_case):
    app.dependency_overrides[get_tag_list_use_case] = lambda: mock_get_tag_list_use_case
    yield
    app.dependency_overrides = {}


def test_get_tag_list_success(authenticated_client, override_dependencies, mock_get_tag_list_use_case, fake_tags):
    client, _ = authenticated_client
    response = client.get("/api/v1/tag", params={"limit": 10})

    mock_get_tag_list_use_case.execute.assert_called_once_with(None, 10)
    assert response.status_code == 200

    json_data = response.json()
    assert "data" in json_data
    assert "metadata" in json_data
    assert len(json_data["data"]) == 10

    first_tag = json_data["data"][0]
    assert first_tag["id"] == fake_tags[0].id
    assert first_tag["name"] == fake_tags[0].name
    assert first_tag["source_address"] == fake_tags[0].source_address
    assert first_tag["description"] == fake_tags[0].description


def test_get_tag_list_failed_unexpectedly(authenticated_client, override_dependencies, mock_get_tag_list_use_case):
    client, _ = authenticated_client
    mock_get_tag_list_use_case.execute.side_effect = Exception("Unexpectedly")

    response = client.get("/api/v1/tag")

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"


def test_end():
    print("\n\nEnd => Get Tag List route\n")
