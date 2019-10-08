import os

import pytest

from mati.resources import Document, ValidateRequest
from mati.types import DocumentType, ValidationInputType, ValidationType

USER = os.getenv('CLIENT_ID')
PASSWORD = os.getenv('CLIENT_SECRET')


@pytest.mark.vcr()
def test_auth(client):
    assert client.token is None
    client._authenticate()
    assert client.token is not None


@pytest.mark.vcr()
def test_identity(client):
    identity = client.create_identity('some_id', 'Pepito Cuenca')
    assert identity


@pytest.mark.vcr()
def test_verification(client):
    identity = client.create_identity('other_id', 'Felipe Lopez Hernandez')
    assert identity
    with open('tests/images/ine.jpg', 'rb') as ff:
        request = ValidateRequest(
            identity_id=identity._id,
            country='MX',
            group=0,
            documents=[
                Document(
                    file_name='tests/images/ine.jpg',
                    stream=ff,
                    validation_type=ValidationType.document,
                    input_type=ValidationInputType.document_photo,
                    document_type=DocumentType.national_id,
                    page='front',
                )
            ],
        )
        validation = client.validate_document(request)
        assert validation.result


@pytest.mark.vcr()
def test_verification_front_back_ine(client):
    identity = client.create_identity('another_id3', 'Felipe Lopez Hernandez')
    assert identity
    with open('tests/images/ine.jpg', 'rb') as ff:
        with open('tests/images/ine2.jpg', 'rb') as ine2:
            with open('tests/images/ine.jpg', 'rb') as ine3:
                with open('tests/images/domicilio.png', 'rb') as comprobante:

                    request = ValidateRequest(
                        identity_id=identity._id,
                        country='MX',
                        group=0,
                        documents=[
                            Document(
                                file_name='tests/images/ine.jpg',
                                stream=ff,
                                validation_type=ValidationType.document,
                                input_type=ValidationInputType.document_photo,
                                document_type=DocumentType.national_id,
                                page='front',
                            ),
                            Document(
                                file_name='tests/images/ine2.jpg',
                                stream=ine2,
                                validation_type=ValidationType.document,
                                input_type=ValidationInputType.document_photo,
                                document_type=DocumentType.national_id,
                                page='back',
                            ),
                            Document(
                                file_name='tests/images/domicilio.png',
                                stream=comprobante,
                                validation_type=ValidationType.document,
                                input_type=ValidationInputType.document_photo,
                                document_type=DocumentType.proof_of_residency,
                            ),
                            Document(
                                file_name='tests/images/ine.jpg',
                                stream=ine3,
                                validation_type=ValidationType.video,
                                input_type=ValidationInputType.selfie_video,
                            ),
                        ],
                    )
                    validation = client.validate_document(request)
                    assert validation.result
