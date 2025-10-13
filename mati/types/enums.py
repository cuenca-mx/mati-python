from dataclasses import dataclass, field, fields
from datetime import date
from enum import Enum
from typing import Any, BinaryIO, Dict, List, Optional, Union


class SerializableEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class PageType(SerializableEnum):
    front = 'front'
    back = 'back'


@dataclass
class BaseModel:
    def __init__(self, **_) -> None:  # pragma: no cover
        ...

    @classmethod
    def _filter_excess_fields(cls, obj_dict: Dict) -> None:
        excess = set(obj_dict.keys()) - {f.name for f in fields(cls)}
        for f in excess:
            del obj_dict[f]

    @classmethod
    def _from_dict(cls, obj_dict: Dict[str, Any]) -> 'BaseModel':
        cls._filter_excess_fields(obj_dict)
        return cls(**obj_dict)


class ValidationInputType(SerializableEnum):
    document_photo = 'document-photo'
    selfie_photo = 'selfie-photo'
    selfie_video = 'selfie-video'


class ValidationType(SerializableEnum):
    driving_license = 'driving-license'
    national_id = 'national-id'
    passport = 'passport'
    proof_of_residency = 'proof-of-residency'
    liveness = 'video/mp4'


@dataclass
class VerificationDocumentStep(BaseModel):
    id: str
    status: int
    error: Optional[Dict] = None
    data: Optional[Dict] = field(default_factory=dict)


@dataclass
class Errors:
    identifier: str
    type: str
    code: str
    message: str


@dataclass
class VerificationDocument(BaseModel):
    country: str
    region: str
    photos: List[str]
    steps: List[VerificationDocumentStep]
    type: str
    subtype: Optional[str] = None
    fields: Optional[dict] = None

    @property
    def errors(self) -> List[Errors]:
        if not self.steps:
            return []
        errors = [
            Errors(
                identifier=step.id,
                type=step.error['type'] if 'type' in step.error else None,
                code=step.error['code'] if 'code' in step.error else None,
                message=step.error['message']
                if 'message' in step.error
                else None,
            )
            for step in self.steps
            if step.error
        ]
        if self.type == 'proof-of-residency' and self.steps:
            step = self.steps[0]
            keys = step.data.keys()  # type: ignore
            required_fileds = []
            for key in keys:
                data = step.data[key]  # type: ignore
                if (
                    'required' in data
                    and data['required']
                    and not data['value']
                ):
                    required_fileds.append(data['label'])
            if required_fileds:
                errors.append(
                    Errors(
                        identifier=step.id,
                        type='StepError',
                        code='document.extractRequiredFields',
                        message=f"We can't extract the following "
                        f"fields in the document: {required_fileds}",
                    )
                )
        return errors

    @property
    def document_type(self) -> str:
        if self.type in ['national-id', 'passport']:
            document_data = [
                step.data
                for step in self.steps
                if step.id == 'document-reading'
            ]
            if document_data[-1] is not None:
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
        return self.type

    @property
    def address(self) -> str:
        """
        This property fills the address direct from the ocr fields `address`
        """
        if self.fields and 'address' in self.fields:
            return self.fields['address']['value']
        return ''

    @property
    def full_name(self) -> str:
        """
        This property fills the fullname direct from the ocr fields `full_name`
        """
        if self.fields and 'full_name' in self.fields:
            return self.fields['full_name']['value']
        return ''

    @property
    def curp(self) -> str:
        """
        This property fills the CURP direct from the ocr fields `curp`
        """
        if self.fields and 'curp' in self.fields:
            return self.fields['curp']['value']
        return ''

    @property
    def document_number(self) -> str:
        """
        This property fills the dni number direct from the ocr
        fields `document_number`
        """
        if self.fields and 'document_number' in self.fields:
            return self.fields['document_number']['value']
        return ''

    @property
    def ocr_number(self) -> str:
        """
        This property fills the number extra direct from the ocr
        fields `ocr_number`
        """
        if self.fields and 'ocr_number' in self.fields:
            return self.fields['ocr_number']['value']
        return ''

    @property
    def expiration_date(self) -> Optional[date]:
        """
        This property fills the expiration date direct from the ocr
        fields `expiration_date`.

        Returns a date object if the field is present and valid.
        Returns None if the field is missing, invalid, or fields is None.
        """
        if self.fields is None:
            return None
        try:
            date_str = self.fields['expiration_date']['value']
            return date.fromisoformat(date_str)
        except (KeyError, TypeError, ValueError):
            return None

    @property
    def emission_date(self) -> Optional[date]:
        """
        This property fills the emission date direct from the ocr
        fields `emission_date`.

        Returns a date object if the field is present and valid.
        Returns None if the field is missing, invalid, or fields is None.
        """
        if self.fields is None:
            return None
        try:
            date_str = self.fields['emission_date']['value']
            return date.fromisoformat(date_str)
        except (KeyError, TypeError, ValueError):
            return None

    def add_expired_step(self) -> None:
        '''
        Appends an expired error step to the document if missing.
        The steps list is used by the errors property.
        This ensures document expiration is reflected
        in the reported errors.
        Required because Metamap does not add this error.
        '''
        step_id = f"{self.type}-document-expired"
        if not any(step.id == step_id for step in self.steps):
            self.steps.append(
                VerificationDocumentStep(
                    id=step_id,
                    status=200,
                    error={
                        'type': 'StepError',
                        'code': 'document.expired',
                        'message': f'Document {self.document_type} expired',
                    },
                )
            )


@dataclass
class LivenessMedia:
    video_url: str
    sprite_url: str
    selfie_url: str


@dataclass
class Liveness(BaseModel):
    status: int
    id: str
    data: Optional[LivenessMedia] = None
    error: Optional[Dict] = None


@dataclass
class DocumentScore:
    is_valid: bool = False
    score: int = 0
    error_codes: Optional[List[str]] = None


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
