import datetime as dt
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional, Union, cast

from ..types.enums import (
    DocumentScore,
    Liveness,
    VerificationDocument,
    VerificationDocumentStep,
)
from .base import Resource


@dataclass
class Verification(Resource):
    _endpoint: ClassVar[str] = '/v2/verifications'

    id: str
    expired: bool
    steps: Optional[List[Liveness]]
    documents: Union[List[VerificationDocument], dict]
    computed: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Dict[str, str]]] = None
    identity: Dict[str, str] = field(default_factory=dict)
    has_problem: Optional[bool] = None
    obfuscated_at: Optional[dt.datetime] = None
    flow: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        docs = []
        self.steps = [Liveness(**step) for step in self.steps]
        for doc in self.documents:
            doc['steps'] = [
                VerificationDocumentStep(**step) for step in doc['steps']
            ]
            docs.append(VerificationDocument(**doc))
        self.documents = docs

    @classmethod
    def retrieve(cls, verification_id: str, client=None) -> 'Verification':
        client = client or cls._client
        endpoint = f'{cls._endpoint}/{verification_id}'
        resp = client.get(endpoint)
        return cast('Verification', cls._from_dict(resp))

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
        pol = [pol for pol in self.steps if pol.id == 'liveness']
        return pol[-1] if pol else None

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
        por = self.proof_of_residency_document
        if not por:
            return None
        return DocumentScore(
            all([step.status == 200 and not step.error for step in por.steps])
            and not (
                self.computed
                and self.computed['is_document_expired']['data'][
                    'proof_of_residency'
                ]
            ),
            sum([step.status for step in por.steps if not step.error]),
            [step.error['code'] for step in por.steps if step.error],
        )

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
        govt = self.govt_id_document
        if not govt:
            return None
        return DocumentScore(
            all(
                [step.status == 200 and not step.error for step in govt.steps]
            ),
            sum([step.status for step in govt.steps if not step.error]),
            [step.error['code'] for step in govt.steps if step.error],
        )
