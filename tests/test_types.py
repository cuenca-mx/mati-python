from datetime import date
from typing import Any, Dict, Optional

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


@pytest.mark.parametrize(
    ('fields', 'expected'),
    [
        (
            {
                'expiration_date': {
                    'value': '2030-12-31',
                    'label': 'Date of Expiration',
                    'format': 'date',
                }
            },
            date(2030, 12, 31),
        ),
        (None, None),
        ({'address': {'value': 'Test Address', 'label': 'Address'}}, None),
        ({'expiration_date': {'label': 'Date of Expiration'}}, None),
    ],
)
def test_expiration_date_property(
    fields: Optional[Dict[str, Any]], expected: Optional[date]
) -> None:
    doc = VerificationDocument(
        country='MX',
        region='',
        photos=[],
        steps=[],
        type='national-id',
        fields=fields,
    )
    assert doc.expiration_date == expected


@pytest.mark.parametrize(
    ('fields', 'expected'),
    [
        (
            {
                'emission_date': {
                    'value': '2023-01-15',
                    'label': 'Emission Date',
                    'format': 'date',
                }
            },
            date(2023, 1, 15),
        ),
        (None, None),
        ({'address': {'value': 'Test Address', 'label': 'Address'}}, None),
        ({'emission_date': {'label': 'Emission Date'}}, None),
    ],
)
def test_emission_date_property(
    fields: Optional[Dict[str, Any]], expected: Optional[date]
) -> None:
    doc = VerificationDocument(
        country='MX',
        region='',
        photos=[],
        steps=[],
        type='proof-of-residency',
        fields=fields,
    )
    assert doc.emission_date == expected
