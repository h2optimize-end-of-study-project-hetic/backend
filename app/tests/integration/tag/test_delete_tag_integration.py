import pytest
import uuid

@pytest.fixture
def tags_created(client, sample_tags_factory, auth_headers):
    tags = sample_tags_factory(1, 3)
    created_tags = []
    for tag in tags:
        payload = {
            "tag": {
                "name": f"{tag.name}_{uuid.uuid4().hex[:8]}",
                "description": tag.description,
                "source_address": f"{tag.source_address}_{uuid.uuid4().hex[:8]}",
            }
        }
        response = client.post("/api/v1/tag", json=payload, headers=auth_headers)
        assert response.status_code == 200, response.json()
        created_tags.append(response.json())
    return created_tags


def test_delete_tag_success(client, tags_created, auth_headers):
    tag_to_delete = tags_created[0]
    tag_id = tag_to_delete["id"]

    response = client.delete(f"/api/v1/tag/{tag_id}", headers=auth_headers)
    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/api/v1/tag/{tag_id}", headers=auth_headers)
    assert get_response.status_code == 404


@pytest.mark.parametrize("tag_id", [-1, 0, "abc"])
def test_delete_tag_failed_invalid_tag_id(client, tag_id, auth_headers):
    response = client.delete(f"/api/v1/tag/{tag_id}", headers=auth_headers)
    assert response.status_code == 422


def test_delete_tag_failed_tag_not_found(client, auth_headers):
    response = client.delete("/api/v1/tag/9999", headers=auth_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Tag with ID '9999' not found"


def test_end():
    print("\n\nEnd => Delete Tag integration\n")
