from enum import Enum


class ValidationInputType(Enum):
    document_photo = 'document-photo'
    selfie_photo = 'selfie-photo'
    selfie_video = 'selfie-video'


class DocumentType(Enum):
    driving_license = 'driving-license'
    national_id = 'national-id'
    passport = 'passport'
    proof_of_residency = 'proof-of-residency'


class ValidationType(Enum):
    document = 'document'
    selfie = 'selfie'
    video = 'video'
