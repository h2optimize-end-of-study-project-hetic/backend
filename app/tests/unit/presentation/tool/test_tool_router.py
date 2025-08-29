from app.src.presentation.core.config import settings
from app.src.domain.entities.role import Role

def test_read_tool_success(authenticated_client):
    client, user = authenticated_client
    assert user.is_active
    assert user.role == Role.admin.value

    response = client.get("/api/v1/tool")
    assert response.status_code == 200

    data = response.json()

    expected = {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "env": settings.ENVIRONMENT,
        "log_level": settings.LOG_LEVEL,
        "debug": settings.is_debug if isinstance(settings.is_debug, bool) else settings.is_debug(),
    }

    for key, value in expected.items():
        assert data[key] == value
