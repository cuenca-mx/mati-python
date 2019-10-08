from mati import Client


def test_create(client: Client):
    at = client.access_tokens.create()
    assert not at.expired
    assert str(at).startswith('Bearer ')
