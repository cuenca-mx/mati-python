import pytest

from mati import Client
from mati.resources import Identity


@pytest.mark.vcr
def test_create_identity(client: Client):
    metadata = dict(
        nombres='Georg Wilhelm',
        primer_apellido='Friedrich',
        segundo_apellido='Hegel',
        dob='1770-08-27',
    )
    identity = client.identities.create(**metadata)
    assert identity.metadata == metadata


@pytest.mark.vcr
def test_retrieve_identity(client: Client, identity: Identity):
    new_identity = client.identities.retrieve(identity.id)
    assert new_identity == identity
    identity.refresh()
    assert new_identity == identity
