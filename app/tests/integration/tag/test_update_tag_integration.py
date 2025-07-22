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


def test_update_tag_success(client, tags_created):
    tag_to_update = tags_created[0]
    tag_id = tag_to_update["id"]
    payload = {
        "tag": {
            "name": "Updated Name",
            "description": "Updated Description",
            "source_address": "updated-src-address",
        }
    }

    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == tag_id
    assert data["name"] == payload["tag"]["name"]
    assert data["description"] == payload["tag"]["description"]
    assert data["source_address"] == payload["tag"]["source_address"]
    assert data["updated_at"] is not None

    get_response = client.get("/api/v1/tag", params={"cursor": f"id={tag_id}", "limit": 1})
    assert get_response.status_code == 200

    retrieved_data = get_response.json()["data"][0]
    assert retrieved_data == data


@pytest.mark.parametrize("tag_id", [-1, 0, "abc"])
def test_update_tag_failed_invalid_tag_id(client, tag_id):
    payload = {
        "tag": {
            "name": "Updated Name",
            "description": "Updated Description",
            "source_address": "updated-src-address",
        }
    }
    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)
    assert response.status_code == 422


def test_update_tag_failed_tag_not_found(client):
    payload = {
        "tag": {
            "name": "Updated Name",
            "description": "Updated Description",
            "source_address": "updated-src-address",
        }
    }
    response = client.patch("/api/v1/tag/9999", json=payload)
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "Tag with ID '9999' not found"


def test_update_tag_failed_already_exists(client, tags_created):
    payload_existing = {
        "tag": {
            "name": "Another Name",
            "description": "Another Description",
            "source_address": tags_created[1]["source_address"],
        }
    }
    response = client.patch(f"/api/v1/tag/{tags_created[0]['id']}", json=payload_existing)
    assert response.status_code == 409

    assert response.json()["detail"] == f"Tag with source_address '{tags_created[1]['source_address']}' already exists"


@pytest.mark.parametrize(
    "payload",
    [
        {"tag": {"name": "ab", "description": "desc", "source_address": "valid-src"}},
        {"tag": {"name": "Valid Name", "description": "desc", "source_address": "x"}},
        {"tag": {"name": "a" * 256, "description": "desc", "source_address": "valid-src"}},
    ],
)
def test_update_tag_failed_invalid_payload(client, tags_created, payload):
    tag_to_update = tags_created[0]
    response = client.patch(f"/api/v1/tag/{tag_to_update['id']}", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "payload, expected_changes",
    [
        ({"tag": {"description": "Updated description"}}, {"description": "Updated description"}),
        ({"tag": {"name": "Updated name"}}, {"name": "Updated name"}),
        ({"tag": {"source_address": "updated-src"}}, {"source_address": "updated-src"}),
        (
            {"tag": {"name": "Full update", "description": "Full desc", "source_address": "full-src"}},
            {"name": "Full update", "description": "Full desc", "source_address": "full-src"},
        ),
        ({"tag": {}}, {}),
    ],
)
def test_update_tag_success_parametrized(client, tags_created, payload, expected_changes):
    tag_to_update = tags_created[0]
    tag_id = tag_to_update["id"]

    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload)
    assert response.status_code == 200

    data = response.json()

    for field, expected_value in expected_changes.items():
        assert data[field] == expected_value

    for field in ["name", "description", "source_address"]:
        if field not in expected_changes:
            assert data[field] == tag_to_update[field]


def test_end():
    print("\n\nEnd => Update Tag integration\n")
