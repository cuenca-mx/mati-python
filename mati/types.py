from dataclasses import dataclass
from enum import Enum
from typing import BinaryIO, Union


class SerializableEnum(str, Enum):
    def __str__(self):
        return self.value


class PageType(SerializableEnum):
    front = 'front'
    back = 'back'


class ValidationInputType(SerializableEnum):
    document_photo = 'document-photo'
    selfie_photo = 'selfie-photo'
    selfie_video = 'selfie-video'


class ValidationType(SerializableEnum):
    driving_license = 'driving-license'
    national_id = 'national-id'
    passport = 'passport'
    proof_of_residency = 'proof-of-residency'


@dataclass
class UserValidationFile:
    filename: str
    content: BinaryIO
    input_type: Union[str, ValidationInputType]
    validation_type: Union[str, ValidationType]
    country: str  # alpha-2 code: https://www.iban.com/country-codes
    region: str = ''  # 2-digit US State code (if applicable)
    group: int = 0
    page: Union[str, PageType] = PageType.front
