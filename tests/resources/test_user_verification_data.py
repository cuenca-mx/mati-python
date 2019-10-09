import os

import pytest

from mati.resources import Identity

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'user_documentation_files'
)


@pytest.mark.vcr
def test_ine_upload(identity: Identity):
    filepath = os.path.join(FIXTURE_DIR, 'ine.jpg')
    with open(filepath, 'rb') as ine:
        uploaded = identity.upload_validation_data(
            filename='ine.jpg',
            content=ine,
            input_type='document-photo',
            validation_type='national-id',
            country='MX',
        )
        assert uploaded is True
