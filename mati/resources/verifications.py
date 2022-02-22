import datetime as dt
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional, cast

from ..types import (
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
    documents: List[VerificationDocument]
    metadata: Optional[Dict[str, Dict[str, str]]] = None
    identity: Dict[str, str] = field(default_factory=dict)
    has_problem: Optional[bool] = None
    computed: Optional[Dict[str, Any]] = None
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
    def proof_of_residency_document(self):
        pors = [
            por for por in self.documents if por.type == 'proof-of-residency'
        ]
        return pors[-1] if pors else None

    @property
    def proof_of_life_document(self):
        pol = [pol for pol in self.steps if pol.id == 'liveness']
        return pol[-1] if pol else None

    @property
    def gov_id_document(self):
        govs = [
            gov
            for gov in self.documents
            if gov.type in ['national-id', 'passport']
        ]
        return govs[-1] if govs else None

    @property
    def proof_of_residency_is_valid(self):
        por = self.proof_of_residency_document
        return DocumentScore(
            all([step.status == 200 for step in por.steps])
            and not self.computed['is_document_expired']['data'][
                'proof_of_residency'
            ],
            sum([step.status for step in por.steps]),
        )

    @property
    def proof_of_life_is_valid(self):
        pol = self.proof_of_life_document
        return DocumentScore(pol.status == 200 and not pol.error, pol.status)

    @property
    def gov_id_is_valid(self):
        gov = self.gov_id_document
        return DocumentScore(
            all([step.status == 200 for step in gov.steps]),
            sum([step.status for step in gov.steps]),
        )
