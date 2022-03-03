# from mati.types import (
#     ValidationInputType,
#     VerificationDocument,
#     VerificationDocumentStep,
# )
#
#
# def test_type_to_str():
#     assert str(ValidationInputType.document_photo) == 'document-photo'
#     assert ValidationInputType.document_photo == 'document-photo'
#
#
# def test_document_type():
#     document = VerificationDocument(
#         country='MX',
#         region='mex',
#         photos=[],
#         steps=[
#             VerificationDocumentStep(
#                 id='document-reading',
#                 status=200,
#                 data={'cde': {'label': 'Elector Key', 'value': 'some'}},
#             )
#         ],
#         type='ine',
#     )
#     assert document.document_type == 'ine'
#     document.type = 'passport'
#     assert document.document_type == 'passport'
