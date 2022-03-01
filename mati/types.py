from dataclasses import dataclass, field
from enum import Enum
from typing import BinaryIO, Dict, List, Optional, Union


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
class VerificationDocumentStep:
    id: str
    status: int
    error: Optional[Dict] = None
    data: Optional[Dict] = field(default_factory=dict)


@dataclass
class VerificationDocument:
    country: str
    region: str
    photos: List[str]
    steps: List[VerificationDocumentStep]
    type: ValidationType
    fields: Optional[dict] = None

    @property
    def document_type(self):
        if self.type in ['national-id', 'passport']:
            document_data = [
                step.data
                for step in self.steps
                if step.id == 'document-reading'
            ]
            if (
                all(
                    [
                        self.type == 'national-id',
                        document_data,
                        'cde' in document_data[-1],
                    ]
                )
                and document_data[-1]['cde']['label'] == 'Elector Key'
                and document_data[-1]['cde']['value']
            ):
                return 'ine'
            elif self.type == 'passport':
                return 'passport'
            else:
                return 'dni'
        else:
            return self.type

    @property
    def address(self):
        """
        This property fills the address direct from the ocr fields `address`
        """
        if 'address' in self.fields:
            return self.fields['address']['value']
        else:
            return None

    @property
    def full_name(self):
        """
        This property fills the fullname direct from the ocr fields `full_name`
        """
        if 'full_name' in self.fields:
            return self.fields['full_name']['value']
        else:
            return None


@dataclass
class LivenessMedia:
    video_url: str
    sprite_url: str
    selfie_url: str


@dataclass
class Liveness:
    status: int
    id: str
    data: LivenessMedia
    error: Optional[Dict]


@dataclass
class DocumentScore:
    is_valid: bool
    score: int
    error_codes: Optional[List[str]]


@dataclass
class UserValidationFile:
    filename: str
    content: BinaryIO
    input_type: Union[str, ValidationInputType]
    validation_type: Union[str, ValidationType] = ''
    country: str = ''  # alpha-2 code: https://www.iban.com/country-codes
    region: str = ''  # 2-digit US State code (if applicable)
    group: int = 0
    page: Union[str, PageType] = PageType.front
