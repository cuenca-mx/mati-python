import os

import pytest

from mati import Client

USER = os.getenv('CLIENT_ID', 'asdasd')
PASSWORD = os.getenv('CLIENT_SECRET', '123')


@pytest.fixture
def client():
    yield Client(client_id=USER, client_secret=PASSWORD)
