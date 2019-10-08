import pytest

from mati import Client


@pytest.mark.vcr
def test_create_access_token(client: Client):
    at = client.access_tokens.create()
    assert not at.expired
    assert str(at).startswith('Bearer ')
