import pytest

from mati import Client
from mati.resources import Identity


@pytest.mark.vcr
def test_user_verification(client: Client, identity: Identity):
    with open('tests/images/ine.jpg', 'rb') as ff:
        user_validation = client.user_validation_data.create(
            identity_id=identity._id,
            filename='tests/images/ine.jpg',
            content=ff,
            input_type='document-photo',
            validation_type='national-id',
            country='MX',
        )
        assert user_validation
