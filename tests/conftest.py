import pytest

from mati import Client


@pytest.fixture
def client():
    # using credentials from env
    yield Client()
