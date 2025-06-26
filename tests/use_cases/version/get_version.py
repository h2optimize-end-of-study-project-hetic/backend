import pytest

class FakeVersionRepository(VersionRepository):
    async def get_version(self) -> Version:
        return Version(name="TestApp", version="0.1.0")


@pytest.mark.asyncio
async def test_get_version_use_case_returns_expected_data():
    fake_repo = FakeVersionRepository()
    use_case = GetVersion(fake_repo)

    result = await use_case.execute()

    assert isinstance(result, Version)
    assert result.name == "TestApp"
    assert result.version == "0.1.0"