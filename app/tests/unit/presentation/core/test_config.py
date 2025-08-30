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
