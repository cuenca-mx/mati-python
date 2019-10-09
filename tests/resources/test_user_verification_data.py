import os

import pytest

from mati.resources import Identity
from mati.types import UserValidationFile, ValidationInputType, ValidationType

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'user_documentation_files'
)


@pytest.mark.vcr
def test_ine_upload(identity: Identity):
    filepath = os.path.join(FIXTURE_DIR, 'ine.jpg')
    with open(filepath, 'rb') as ine:
        user_validation_file = UserValidationFile(
            filename='ine.jpg',
            content=ine,
            input_type=ValidationInputType.document_photo,
            validation_type=ValidationType.national_id,
            country='MX',
        )
        uploaded = identity.upload_validation_data([user_validation_file])
    assert uploaded is True
