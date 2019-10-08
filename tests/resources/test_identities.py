import pytest

from mati import Client


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
