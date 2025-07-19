import pytest


@pytest.fixture
def tags_created(client, sample_tags_factory):
    tags = sample_tags_factory(1, 3)
    created_tags = []
    for tag in tags:
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


def test_delete_tag_success(client, tags_created):
    tag_to_delete = tags_created[0]
    tag_id = tag_to_delete["id"]

    response = client.delete(f"/api/v1/tag/{tag_id}")
    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/api/v1/tag/{tag_id}")
    assert get_response.status_code == 404


@pytest.mark.parametrize("tag_id", [-1, 0, "abc"])
def test_delete_tag_failed_invalid_tag_id(client, tag_id):
    response = client.delete(f"/api/v1/tag/{tag_id}")
    assert response.status_code == 422


def test_delete_tag_failed_tag_not_found(client):
    response = client.delete("/api/v1/tag/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Tag with ID '9999' not found"


def test_end():
    print("\n\nEnd => Delete Tag integration\n")
