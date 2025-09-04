import pytest
import uuid

@pytest.fixture
def tags_created(client, auth_headers):
    """Crée plusieurs tags uniques pour les tests."""
    created_tags = []
    for i in range(1, 4):
        payload = {
            "tag": {
                "name": f"Tag {i}_{uuid.uuid4().hex[:6]}",
                "description": "desc",
                "source_address": f"src-{uuid.uuid4().hex[:6]}",
            }
        }
        response = client.post("/api/v1/tag", json=payload, headers=auth_headers)
        assert response.status_code == 200
        created_tags.append(response.json())
    return created_tags



def test_update_tag_failed_tag_not_found(client, auth_headers):
    payload = {
        "tag": {
            "name": "Updated Name",
            "description": "Updated Description",
            "source_address": f"src-{uuid.uuid4().hex[:6]}",
        }
    }
    response = client.patch("/api/v1/tag/9999", json=payload, headers=auth_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Tag with ID '9999' not found"

def test_update_tag_failed_already_exists(client, tags_created, auth_headers):
    payload_existing = {
        "tag": {
            "name": "Another Name",
            "description": "Another Description",
            "source_address": tags_created[1]["source_address"],  # conflit
        }
    }
    response = client.patch(f"/api/v1/tag/{tags_created[0]['id']}", json=payload_existing, headers=auth_headers)
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
def test_update_tag_failed_invalid_payload(client, tags_created, payload, auth_headers):
    tag_to_update = tags_created[0]
    response = client.patch(f"/api/v1/tag/{tag_to_update['id']}", json=payload, headers=auth_headers)
    assert response.status_code == 422

@pytest.mark.parametrize(
    "payload, expected_changes",
    [
        ({"tag": {"description": "Updated description"}}, {"description": "Updated description"}),
        ({"tag": {"name": "Updated name"}}, {"name": "Updated name"}),
        ({"tag": {}}, {}),
    ],
)
def test_update_tag_success_parametrized(client, tags_created, payload, expected_changes, auth_headers):
    tag_to_update = tags_created[0]
    tag_id = tag_to_update["id"]

    response = client.patch(f"/api/v1/tag/{tag_id}", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    for field, expected_value in expected_changes.items():
        assert data[field] == expected_value

    for field in ["name", "description", "source_address"]:
        if field not in expected_changes:
            assert data[field] == tag_to_update[field]

def test_end():
    print("\n\nEnd => Update Tag integration\n")
