import pytest
from pytest_lazyfixture import lazy_fixture

from mati.types import ValidationInputType


def test_type_to_str():
    assert str(ValidationInputType.document_photo) == 'document-photo'


@pytest.mark.parametrize(
    ('verification_document', 'expected_type'),
    (
        (
            lazy_fixture('verification_document_national_id'),
            'ine',
        ),
        (
            lazy_fixture('verification_document_passport'),
            'passport',
        ),
        (
            lazy_fixture('verification_document_dni'),
            'dni',
        ),
        (
            lazy_fixture('verification_document_foreign_id'),
            'foreign-id',
        ),
    ),
)
def test_document_type(verification_document, expected_type):
    assert verification_document.document_type == expected_type
