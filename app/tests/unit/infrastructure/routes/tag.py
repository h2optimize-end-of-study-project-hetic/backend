from fastapi.testclient import TestClient
from app.presentation.main import app
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository

# 🧪 Fake repository pour tests
class FakeUserRepository(UserRepository):
    def create(self, user: User) -> User:
        return User(id=1, name=user.name)  # simulate a saved user

# 🪄 On override la dépendance
def override_get_user_repository():
    return FakeUserRepository()

app.dependency_overrides[
    # même signature que Depends()
    "app.presentation.api.deps.get_user_repository"
] = override_get_user_repository

client = TestClient(app)

def test_create_user():
    response = client.post("/api/users", json={"name": "Jean"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jean"
    assert data["id"] == 1
