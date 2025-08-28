import pytest
import uuid


@pytest.fixture
def fake_tag(sample_tags_factory):
    return sample_tags_factory(1, 2)[0]


@pytest.fixture
def tag_created(client, fake_tag, auth_headers):
    payload = {
        "tag": {
            "name": f"{fake_tag.name}_{uuid.uuid4().hex[:8]}",
            "description": fake_tag.description,
            "source_address": f"{fake_tag.source_address}_{uuid.uuid4().hex[:8]}",
        }
    }
    response = client.post("/api/v1/tag", json=payload, headers=auth_headers)
    assert response.status_code == 200, response.json()
    return response.json()


def test_get_tag_by_id_success(client, tag_created, auth_headers):
    tag_id = tag_created["id"]
    response = client.get(f"/api/v1/tag/{tag_id}", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == tag_created["id"]
    assert data["name"] == tag_created["name"]
    assert data["description"] == tag_created["description"]
    assert data["source_address"] == tag_created["source_address"]
    assert data["created_at"] == tag_created["created_at"]
    assert data["updated_at"] == tag_created["updated_at"]


@pytest.mark.parametrize("tag_id", [-1, 0, "abc"])
def test_get_tag_by_id_failed_invalid_tag_id(client, tag_id, auth_headers):
    response = client.get(f"/api/v1/tag/{tag_id}", headers=auth_headers)
    assert response.status_code == 422


def test_get_tag_by_id_failed_not_found(client, auth_headers):
    response = client.get("/api/v1/tag/9999", headers=auth_headers)
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "Tag with ID '9999' not found"


def test_end():
    print("\n\nEnd => Get Tag by ID integration\n")
