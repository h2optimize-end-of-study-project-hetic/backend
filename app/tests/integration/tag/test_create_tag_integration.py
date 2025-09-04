import pytest
import uuid


@pytest.fixture
def payload_valid():
    """Données valides toujours uniques grâce à un UUID."""
    return {
        "tag": {
            "name": f"Tag-{uuid.uuid4().hex[:6]}",
            "description": "desc",
            "source_address": f"addr_{uuid.uuid4().hex}",
        }
    }


def test_create_tag_and_retrieve_success(client, payload_valid, auth_headers):
    response = client.post("/api/v1/tag", json=payload_valid, headers=auth_headers)
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["name"] == payload_valid["tag"]["name"]
    assert data["description"] == payload_valid["tag"]["description"]
    assert data["source_address"] == payload_valid["tag"]["source_address"]
    assert data["updated_at"] is None

    get_response = client.get(f"/api/v1/tag/{data['id']}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json() == data



def test_create_tag_failed_same_source_address(client, auth_headers):
    # Générer un source_address unique pour être sûr qu'il n'existe pas déjà
    addr = f"addr_{uuid.uuid4().hex}"

    payload = {
        "tag": {
            "name": "Tag Unique",
            "description": "desc",
            "source_address": addr,
        }
    }

    # 1. Création OK
    first_response = client.post("/api/v1/tag", json=payload, headers=auth_headers)
    assert first_response.status_code == 200

    # 2. Doublon attendu
    second_response = client.post("/api/v1/tag", json=payload, headers=auth_headers)
    assert second_response.status_code == 409
    assert "already exists" in second_response.json()["detail"]


@pytest.mark.parametrize(
    "payload",
    [
        ({"tag": {"name": "ab", "description": "desc", "source_address": "valid-src"}},),
        ({"tag": {"name": "Valid Name", "description": "desc", "source_address": "x"}},),
        ({"tag": {"name": "a" * 256, "description": "desc", "source_address": "valid-src"}},),
        ({"tag": {"description": "desc", "source_address": "valid-src"}},),
        ({"tag": {"name": "Valid Name", "description": "desc"}},),
    ],
)
def test_create_tag_invalid_data(client, payload, auth_headers):
    response = client.post("/api/v1/tag", json=payload, headers=auth_headers)
    assert response.status_code == 422


def test_end():
    print("\n\nEnd => Create Tag integration\n")
