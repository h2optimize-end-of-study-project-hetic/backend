from app.application.use_cases.create_user import CreateUserUseCase
from app.domain.models.user import User

class FakeRepo:
    def create(self, user: User):
        return user

def test_create_user():
    uc = CreateUserUseCase(FakeRepo())
    u = User(id=None, name='Jean')
    assert uc.execute(u).name == 'Jean'


def override_use_case():
    class FakeUC:
        def execute(self, tag_id: int):
            return {
                "id": tag_id,
                "name": "MockTag",
                "description": "Fake",
                "source_address": "0x123",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": None
            }
    return FakeUC()

app.dependency_overrides[get_tag_by_id_use_case] = override_use_case