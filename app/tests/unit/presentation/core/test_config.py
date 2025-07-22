from app.src.presentation.core.config import Settings


def test_is_debug_property_dev_debug():
    s = Settings(ENVIRONMENT="development", DEBUG=False)
    assert s.is_debug is True


def test_is_debug_property_prod_debug():
    s = Settings(ENVIRONMENT="production", DEBUG=True)
    assert s.is_debug is True


def test_is_debug_property_prod():
    s = Settings(ENVIRONMENT="production", DEBUG=False)
    assert s.is_debug is False


def test_openapi_url_property_dev():
    s = Settings(ENVIRONMENT="development", API_V1_STR="/api/v1")
    assert s.openapi_url == "/api/v1/openapi.json"


def test_openapi_url_property_prod():
    s = Settings(ENVIRONMENT="production")
    assert s.openapi_url is None
