import pytest

from mati.resources import Identity


@pytest.mark.vcr
def test_user_verification(identity: Identity):
    with open('tests/images/ine.jpg', 'rb') as ine:
        uploaded = identity.upload_validation_data(
            filename='ine.jpg',
            content=ine,
            input_type='document-photo',
            validation_type='national-id',
            country='MX',
        )
        assert uploaded is True
