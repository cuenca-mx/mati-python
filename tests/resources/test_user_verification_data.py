import os

import pytest

from mati.resources import Identity
from mati.types import (
    PageType,
    UserValidationFile,
    ValidationInputType,
    ValidationType,
)

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'user_documentation_files'
)


@pytest.mark.vcr
def test_ine_and_liveness_upload(identity: Identity):
    filepath_front = os.path.join(FIXTURE_DIR, 'ine_front.jpg')
    filepath_back = os.path.join(FIXTURE_DIR, 'ine_back.jpg')
    filepath_live = os.path.join(FIXTURE_DIR, 'liveness.MOV')
    with open(filepath_front, 'rb') as front, open(
        filepath_back, 'rb'
    ) as back, open(filepath_live, 'rb') as live:
        user_validation_file = UserValidationFile(
            filename='ine_front.jpg',
            content=front,
            input_type=ValidationInputType.document_photo,
            validation_type=ValidationType.national_id,
            country='MX',
        )
        user_validation_file_back = UserValidationFile(
            filename='ine_back.jpg',
            content=back,
            input_type=ValidationInputType.document_photo,
            validation_type=ValidationType.national_id,
            country='MX',
            page=PageType.back,
        )
        user_validation_live = UserValidationFile(
            filename='liveness.MOV',
            content=live,
            input_type=ValidationInputType.selfie_video,
        )
        resp = identity.upload_validation_data(
            [
                user_validation_file,
                user_validation_file_back,
                user_validation_live,
            ]
        )
    assert all([resp[i]['result'] for i in range(3)]) is True
