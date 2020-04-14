import datetime as dt
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Union

from ..types import UserValidationFile
from .base import Resource
from .user_verification_data import UserValidationData


@dataclass
class Identity(Resource):
    """
    Based on: https://docs.getmati.com/#step-2-create-a-new-identity
    """

    _endpoint: ClassVar[str] = '/v2/identities'

    id: str
    dateCreated: dt.datetime
    dateUpdated: dt.datetime
    alive: Optional[bool]
    status: str
    annotatedStatus: Optional[str] = None
    user: Optional[str] = None
    metadata: Union[dict, List[str]] = field(default_factory=dict)
    fullName: Optional[str] = None
    facematchScore: Optional[float] = None
    photo: Optional[str] = None
    video: Optional[str] = None
    flowId: Optional[str] = None

    @classmethod
    def create(cls, client=None, **metadata) -> 'Identity':
        client = client or cls._client
        resp = client.post(cls._endpoint, json=dict(metadata=metadata))
        resp['id'] = resp.pop('_id')
        return cls(**resp)

    @classmethod
    def retrieve(cls, identity_id: str, client=None) -> 'Identity':
        client = client or cls._client
        endpoint = f'{cls._endpoint}/{identity_id}'
        resp = client.get(endpoint)
        resp['id'] = resp.pop('_id')
        return cls(**resp)

    def refresh(self, client=None) -> None:
        client = client or self._client
        identity = self.retrieve(self.id, client=client)
        for k, v in identity.__dict__.items():
            setattr(self, k, v)

    def upload_validation_data(
        self, user_validation_files: List[UserValidationFile], client=None
    ) -> List[dict]:
        client = client or self._client
        return UserValidationData.upload(
            self.id, user_validation_files, client=client
        )
