from app.application.use_cases.create_user import CreateUserUseCase
from app.domain.models.user import User

class FakeRepo:
    def create(self, user: User):
        return user

def test_create_user():
    uc = CreateUserUseCase(FakeRepo())
    u = User(id=None, name='Jean')
    assert uc.execute(u).name == 'Jean'
