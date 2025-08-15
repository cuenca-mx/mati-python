import datetime as dt
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional, Union, cast

from ..types.enums import (
    DocumentScore,
    Errors,
    Liveness,
    UserValidationFile,
    VerificationDocument,
    VerificationDocumentStep,
)
from .base import Resource
from .user_verification_data import UserValidationData


@dataclass
class Verification(Resource):
    _endpoint: ClassVar[str] = '/v2/verifications'

    id: str
    expired: bool
    steps: Optional[List[Liveness]]
    documents: Union[List[VerificationDocument], dict]
    computed: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    identity: Dict[str, str] = field(default_factory=dict)
    has_problem: Optional[bool] = None
    obfuscated_at: Optional[dt.datetime] = None
    flow: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        docs = []
        self.steps = [Liveness._from_dict(step) for step in self.steps]
        for doc in self.documents:
            doc['steps'] = [
                VerificationDocumentStep._from_dict(step)
                for step in doc['steps']
            ]
            docs.append(VerificationDocument._from_dict(doc))
        self.documents = docs

    @classmethod
    def create(cls, flow_id: str, client=None, **metadata):
        client = client or cls._client
        resp = client.post(
            cls._endpoint, json=dict(flowId=flow_id, metadata=metadata)
        )
        return cast('Verification', cls._from_dict(resp))

    @classmethod
    def retrieve(cls, verification_id: str, client=None) -> 'Verification':
        client = client or cls._client
        endpoint = f'{cls._endpoint}/{verification_id}'
        resp = client.get(endpoint)
        return cast('Verification', cls._from_dict(resp))

    @classmethod
    def upload_validation_data(
        cls,
        user_validation_files: List[UserValidationFile],
        identity_id: str,
        client=None,
    ) -> List[dict]:
        client = client or cls._client
        return UserValidationData.upload(
            identity_id, user_validation_files, client=client
        )

    @property
    def is_pending(self) -> bool:
        return self.identity['status'] in ['running', 'pending']

    @property
    def proof_of_residency_document(self) -> Optional[VerificationDocument]:
        pors = [
            por for por in self.documents if por.type == 'proof-of-residency'
        ]
        return pors[-1] if pors else None

    @property
    def proof_of_life_document(self) -> Optional[Liveness]:
        if not self.steps:
            return None
        pol = [pol for pol in self.steps if pol.id in ['liveness', 'selfie']]
        return pol[-1] if pol else None

    @property
    def proof_of_life_url(self) -> Optional[str]:
        pol = self.proof_of_life_document
        if not pol:
            return None
        data = getattr(pol, 'data', {}) or {}
        return data.get('video_url') or data.get('selfie_photo_url')

    @property
    def proof_of_life_errors(self) -> List[Errors]:
        return [
            Errors(
                identifier=pol.id,
                type=pol.error['type'] if 'type' in pol.error else None,
                code=pol.error['code'] if 'code' in pol.error else None,
                message=pol.error['message']
                if 'message' in pol.error
                else None,
            )
            for pol in self.steps  # type: ignore
            if pol.id in ['liveness', 'selfie'] and pol.error
        ]

    @property
    def govt_id_document(self) -> Optional[VerificationDocument]:
        govs = [
            govt
            for govt in self.documents
            if govt.type in ['national-id', 'passport']
        ]
        return govs[-1] if govs else None

    @property
    def proof_of_residency_validation(self) -> Optional[DocumentScore]:
        return self.get_document_validation(self.proof_of_residency_document)

    @property
    def proof_of_life_validation(self) -> Optional[DocumentScore]:
        pol = self.proof_of_life_document
        if not pol:
            return None
        return DocumentScore(
            pol.status == 200 and not pol.error,
            pol.status,
            [pol.error['type']] if pol.error else [],
        )

    @property
    def govt_id_validation(self) -> Optional[DocumentScore]:
        return self.get_document_validation(self.govt_id_document)

    def get_document_validation(
        self, document: Optional[VerificationDocument]
    ) -> Optional[DocumentScore]:
        if not document:
            return None
        document_type = document.type.replace("-", "_")
        is_expired = (
            self.computed['is_document_expired']['data'][document_type]
            if self.computed
            else False
        )
        if is_expired:
            document.add_expired_step()
        return DocumentScore(
            all(
                [
                    step.status == 200 and not step.error
                    for step in document.steps
                ]
            ),
            sum([step.status for step in document.steps if not step.error]),
            [step.error['code'] for step in document.steps if step.error],
        )
