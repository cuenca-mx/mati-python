import datetime as dt
from dataclasses import dataclass
from typing import ClassVar

from .base import Resource
from .user_verification_data import UserValidationData


@dataclass
class Identity(Resource):
    """
    Based on: https://docs.getmati.com/#step-2-create-a-new-identity
    """

    _endpoint: ClassVar[str] = '/v2/identities'

    _id: str
    dateCreated: dt.datetime
    dateUpdated: dt.datetime
    alive: None  # At the moment, this always comes back as None
    metadata: dict
    status: str
    user: str

    @classmethod
    def create(cls, **metadata) -> 'Identity':
        resp = cls._client.post(cls._endpoint, json=dict(metadata=metadata))
        return cls(**resp)

    def upload_validation_data(self, **kwargs) -> UserValidationData:
        return UserValidationData.create(self._id, **kwargs)
