import pytest

from mati import Client
from mati.resources import Resource


@pytest.mark.vcr()
def test_two_clients():
    secondary_client = Client('test', 'test')
    main_client = Client('api_key', 'secret_key')

    # NOTE: Resource._client is the default client for requests and
    # always has the reference to the last client initialized
    assert Resource._client == main_client

    assert main_client.bearer_token is None
    assert secondary_client.bearer_token is None

    metadata = dict(
        nombres='Georg Wilhelm',
        primer_apellido='Friedrich',
        segundo_apellido='Hegel',
        dob='1770-08-27',
    )

    main_identity = main_client.identities.create(**metadata)
    secondary_identity = secondary_client.identities.create(
        client=secondary_client, **metadata
    )

    main_retrieve = main_client.identities.retrieve(main_identity.id)
    secondary_retrieve = secondary_client.identities.retrieve(
        secondary_identity.id, client=secondary_client
    )
    assert main_retrieve.id == main_identity.id
    assert secondary_retrieve.id == secondary_identity.id

    assert main_client.bearer_token == main_client.get_valid_bearer_token()
