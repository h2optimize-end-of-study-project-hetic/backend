from base64 import urlsafe_b64encode, urlsafe_b64decode
import json
from urllib.parse import urlencode, parse_qs

from app.src.common.exception import DecodedFailedException

def encode(data: dict) -> str:
    return urlencode(data)

def decode(cursor: str, resource_name: str = 'Unknow element') -> dict:
    try:
        parsed = parse_qs(cursor)
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
    except Exception as e:
        raise DecodedFailedException(resource_name, str(e)) from e
