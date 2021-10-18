import pytest
from requests.exceptions import HTTPError

from mati import Client


@pytest.mark.vcr
def test_client_renew_access_token():
    client = Client('api_key', 'secret_key')
    assert client.bearer_token is None
    client.get_valid_bearer_token()
    assert not client.bearer_token.expired
    assert client.bearer_token == client.get_valid_bearer_token()


@pytest.mark.vcr
def test_failed_auth():
    client = Client('wrong', 'creds')
    with pytest.raises(HTTPError) as exc_info:
        client.access_tokens.create()
    assert exc_info.value.response.status_code == 401
