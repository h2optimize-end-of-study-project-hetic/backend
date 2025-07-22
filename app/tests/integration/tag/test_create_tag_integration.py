import pytest


@pytest.fixture
def fake_tag(sample_tags_factory):
    return sample_tags_factory(1, 2)[0]


@pytest.fixture
def payload_valid(fake_tag):
    return {
        "tag": {
            "name": fake_tag.name,
            "description": fake_tag.description,
            "source_address": fake_tag.source_address,
        }
    }


def test_create_tag_and_retrieve_success(client, payload_valid):
    response = client.post("/api/v1/tag", json=payload_valid)
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["name"] == payload_valid["tag"]["name"]
    assert data["description"] == payload_valid["tag"]["description"]
    assert data["source_address"] == payload_valid["tag"]["source_address"]
    assert data["updated_at"] is None

    get_response = client.get(f"/api/v1/tag/{data['id']}")
    assert get_response.status_code == 200

    retrieved_data = get_response.json()
    assert retrieved_data == data

    response1 = client.post("/api/v1/tag", json=payload_valid)
    assert response1.status_code == 409


def test_create_tag_failed_same_source_address(client, payload_valid):
    response = client.post("/api/v1/tag", json=payload_valid)
    assert response.status_code == 200


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
def test_create_tag_invalid_data(client, payload):
    response = client.post("/api/v1/tag", json=payload)
    assert response.status_code == 422


def test_end():
    print("\n\nEnd => Create Tag integration\n")
