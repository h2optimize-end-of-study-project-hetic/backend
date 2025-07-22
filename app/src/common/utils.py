from urllib.parse import parse_qs, urlencode

from app.src.common.exception import DecodedFailedError


def encode(data: dict) -> str:
    return urlencode(data)


def decode(cursor: str, resource_name: str = "Unknown element") -> dict:
    parsed = parse_qs(cursor)
    if not parsed:
        raise DecodedFailedError(resource_name, "Decoded value is empty")
    return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
