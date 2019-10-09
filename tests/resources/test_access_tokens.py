import pytest

from mati import Client


@pytest.mark.vcr
def test_create_access_token(client: Client):
    token = client.access_tokens.create()
    assert not token.expired
    assert str(token).startswith('Bearer ')


@pytest.mark.vcr
def test_created_scored_token(client: Client):
    scored = client.access_tokens.create('identity')
    assert not scored.expired
    assert scored.score == 'identity'
