import pytest
import uuid


@pytest.fixture
def fakes_tag(sample_tags_factory):
    return sample_tags_factory(1, 6)


@pytest.fixture
def tags_created(client, fakes_tag, auth_headers):
    created_tags = []
    for tag in fakes_tag:
        unique_suffix = uuid.uuid4().hex[:6]
        payload = {
            "tag": {
                "name": f"{tag.name}_{unique_suffix}",
                "description": tag.description,
                "source_address": f"{tag.source_address}_{unique_suffix}",
            }
        }
        response = client.post("/api/v1/tag", json=payload, headers=auth_headers)
        if response.status_code not in (200, 201):
            raise Exception(f"Failed to create tag: {response.status_code} {response.text}")
        created_tags.append(response.json())
    return created_tags


@pytest.mark.parametrize(
    "query_param, expected_status",
    [
        ({"limit": 0}, 422),
        ({"cursor": "invalid_cursor"}, 500)
    ],
)
def test_get_tag_list_invalid_params(client, tags_created, query_param, expected_status, auth_headers):
    response = client.get("/api/v1/tag", params=query_param, headers=auth_headers)
    assert response.status_code == expected_status


def test_end():
    print("\n\nEnd => Get Tag List integration\n")
