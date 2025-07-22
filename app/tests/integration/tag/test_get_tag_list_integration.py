import pytest


@pytest.fixture
def fakes_tag(sample_tags_factory):
    return sample_tags_factory(1, 6)


@pytest.fixture
def tags_created(client, fakes_tag):
    created_tags = []
    for tag in fakes_tag:
        payload = {
            "tag": {
                "name": tag.name,
                "description": tag.description,
                "source_address": tag.source_address,
            }
        }
        response = client.post("/api/v1/tag", json=payload)
        assert response.status_code == 200
        created_tags.append(response.json())
    return created_tags


def test_get_tag_list_success(client):
    response = client.get("/api/v1/tag")
    assert response.status_code == 200


def test_get_tag_list_success_limit(client, tags_created):
    response = client.get("/api/v1/tag", params={"limit": 2})
    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert "metadata" in data

    tags = data["data"]
    metadata = data["metadata"]

    assert isinstance(tags, list)
    assert len(tags) <= 2

    assert metadata["total"] == 5
    assert metadata["chunk_size"] == 2
    assert metadata["chunk_count"] == 3
    assert metadata["current_cursor"] == "id=1"
    assert metadata["first_cursor"] == "id=1"
    assert metadata["last_cursor"] == "id=5"
    assert metadata["next_cursor"] == "id=3"


def test_get_tag_list_with_cursor(client, tags_created):
    response = client.get("/api/v1/tag", params={"limit": 2})
    assert response.status_code == 200

    data = response.json()
    tags = data["data"]
    metadata = data["metadata"]

    assert isinstance(tags, list)
    assert len(tags) == 2
    assert tags[0]["id"] == 1

    assert metadata["total"] == 5
    assert metadata["chunk_size"] == 2
    assert metadata["chunk_count"] == 3
    assert metadata["current_cursor"] == "id=1"
    assert metadata["first_cursor"] == "id=1"
    assert metadata["last_cursor"] == "id=5"
    assert metadata["next_cursor"] == "id=3"

    response2 = client.get("/api/v1/tag", params={"cursor": metadata["next_cursor"], "limit": 2})
    assert response2.status_code == 200
    data2 = response2.json()
    tags2 = data2["data"]
    metadata2 = data2["metadata"]

    assert isinstance(tags, list)
    assert len(tags2) == 2
    assert tags2[0]["id"] == 3

    assert metadata2["total"] == 5
    assert metadata2["chunk_size"] == 2
    assert metadata2["chunk_count"] == 3
    assert metadata2["current_cursor"] == "id=3"
    assert metadata2["first_cursor"] == "id=1"
    assert metadata2["last_cursor"] == "id=5"
    assert metadata2["next_cursor"] == "id=5"

    response3 = client.get("/api/v1/tag", params={"cursor": metadata2["next_cursor"], "limit": 2})
    assert response3.status_code == 200
    data3 = response3.json()
    tags3 = data3["data"]
    metadata3 = data3["metadata"]

    assert isinstance(tags, list)
    assert len(tags3) == 1
    assert tags3[0]["id"] == 5

    assert metadata3["total"] == 5
    assert metadata3["chunk_size"] == 1
    assert metadata3["chunk_count"] == 3
    assert metadata3["current_cursor"] == "id=5"
    assert metadata3["first_cursor"] == "id=1"
    assert metadata3["last_cursor"] == "id=5"
    assert metadata3["next_cursor"] is None


@pytest.mark.parametrize(
    "query_param, expected_status",
    [
        ({"limit": 0}, 422),
        ({"cursor": "invalid_cursor"}, 500),
        ({"cursor": "id=0"}, 200),
    ],
)
def test_get_tag_list_invalid_params(client, tags_created, query_param, expected_status):
    response = client.get("/api/v1/tag", params=query_param)
    assert response.status_code == expected_status


def test_end():
    print("\n\nEnd => Get Tag List integration\n")
