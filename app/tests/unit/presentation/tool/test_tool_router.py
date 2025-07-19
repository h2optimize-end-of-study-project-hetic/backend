from app.src.presentation.core.config import settings

def test_read_tool_success(client):
    response = client.get("/api/v1/tool")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == settings.PROJECT_NAME
    assert data["version"] == settings.VERSION
    assert data["env"] == settings.ENVIRONMENT
    assert data["log_level"] == settings.LOG_LEVEL
    assert data["debug"] == settings.is_debug


def test_end():
    print("\n\nEnd => Tool route\n")