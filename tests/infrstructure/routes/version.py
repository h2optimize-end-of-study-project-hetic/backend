from fastapi.testclient import TestClient
from src.infrastructure.http.api.routes.version import create_version_router
from src.domain.version import Version

class FakeUseCase:
    async def execute(self):
        return Version(name="TEST", version="0.0.0")

def test_route():
    app = FastAPI()
    app.include_router(create_version_router(FakeUseCase()))
    client = TestClient(app)

    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["content"]["name"] == "TEST"