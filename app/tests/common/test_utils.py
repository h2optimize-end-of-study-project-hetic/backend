import pytest

from app.src.common.utils import encode, decode
from app.src.common.exception import DecodedFailedError


def test_encode_dict():
    data = {"id": "123", "name": "test"}
    result = encode(data)
    assert result == "id=123&name=test"


def test_decode_success():
    cursor = "id=123&name=test"
    result = decode(cursor)
    assert result == {"id": "123", "name": "test"}


def test_decode_success_with_multiple_values():
    cursor = "id=123&id=456"
    result = decode(cursor)
    assert result == {"id": ["123", "456"]}


def test_decode_failure_decode_failed_error():
    invalid_cursor = "id123"

    with pytest.raises(DecodedFailedError) as exc_info:
        decode(invalid_cursor, "Tag")

    assert "Failed to decode Tag" in str(exc_info.value)
