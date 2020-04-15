import datetime as dt
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional

from ..types import VerificationDocument, VerificationDocumentStep
from .base import Resource


@dataclass
class Verification(Resource):
    _endpoint: ClassVar[str] = '/api/v1/verifications'
    _token_score: ClassVar[str] = 'identity'

    id: str
    expired: bool
    steps: list
    documents: List[VerificationDocument]
    metadata: Dict[str, Dict[str, str]]
    identity: Dict[str, str] = field(default_factory=dict)
    hasProblem: Optional[bool] = None
    computed: Optional[Dict[str, Any]] = None
    obfuscatedAt: Optional[dt.datetime] = None
    flow: Optional[Dict[str, Any]] = None

    @classmethod
    def retrieve(cls, verification_id: str, client=None) -> 'Verification':
        client = client or cls._client
        endpoint = f'{cls._endpoint}/{verification_id}'
        resp = client.get(endpoint, token_score=cls._token_score)
        docs = []
        for doc in resp['documents']:
            doc['steps'] = [
                VerificationDocumentStep(**step) for step in doc['steps']
            ]
            docs.append(VerificationDocument(**doc))
        resp['documents'] = docs
        return cls(**resp)
