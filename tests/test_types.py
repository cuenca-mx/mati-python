from mati.types import ValidationInputType


def test_type_to_str():
    assert str(ValidationInputType.document_photo) == 'document-photo'
    assert ValidationInputType.document_photo == 'document-photo'
