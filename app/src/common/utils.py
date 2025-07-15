from urllib.parse import parse_qs, urlencode

from app.src.common.exception import DecodedFailedError


def encode(data: dict) -> str:
    return urlencode(data)


def decode(cursor: str, resource_name: str = "Unknow element") -> dict:
    try:
        parsed = parse_qs(cursor)
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
    except Exception as e:
        raise DecodedFailedError(resource_name, str(e)) from e
