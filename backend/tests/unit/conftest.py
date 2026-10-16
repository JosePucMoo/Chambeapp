import pytest

@pytest.fixture(autouse=True)
def unstub():
    from mockito import unstub
    yield
    unstub()
