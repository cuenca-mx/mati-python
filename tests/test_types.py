import pytest
from pytest_lazyfixture import lazy_fixture

from mati.types import ValidationInputType
from mati.types.enums import VerificationDocument, VerificationDocumentStep


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


def test_from_dict():
    data = {'some': 'data', 'aditional': 'data', 'id': 'foo', 'status': 10}
    step = VerificationDocumentStep._from_dict(data)
    assert step


def test_excess_fields():
    data = {'some': 'data', 'aditional': 'data', 'id': 'foo', 'status': 10}
    VerificationDocumentStep._filter_excess_fields(data)
    assert 'some' not in data


def test_expiration_date_property():
    doc = VerificationDocument(
        country='MX',
        region='',
        photos=[],
        steps=[],
        type='national-id',
        fields={
            'expiration_date': {
                'value': '2030-12-31',
                'label': 'Date of Expiration',
                'format': 'date',
            }
        },
    )
    assert doc.expiration_date == '2030-12-31'
    doc_no_fields = VerificationDocument(
        country='MX',
        region='',
        photos=[],
        steps=[],
        type='national-id',
        fields=None,
    )
    assert doc_no_fields.expiration_date == ''


def test_emission_date_property():
    doc = VerificationDocument(
        country='MX',
        region='',
        photos=[],
        steps=[],
        type='proof-of-residency',
        fields={
            'emission_date': {
                'value': '2023-01-15',
                'label': 'Emission Date',
                'format': 'date',
            }
        },
    )
    assert doc.emission_date == '2023-01-15'
    doc_no_fields = VerificationDocument(
        country='MX',
        region='',
        photos=[],
        steps=[],
        type='proof-of-residency',
        fields=None,
    )
    assert doc_no_fields.emission_date == ''
