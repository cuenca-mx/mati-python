import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, Optional

from .base import Resource


@dataclass
class Identity(Resource):
    """
    Based on: https://docs.getmati.com/#step-2-create-a-new-identity
    """

    _endpoint: ClassVar[str] = '/v2/identities'

    _id: str
    dateCreated: dt.datetime
    dateUpdated: dt.datetime
    alive: Optional[bool]  # assuming it's a bool. Docs are not clear
    metadata: dict
    status: str
    user: str

    @classmethod
    def create(cls, **metadata) -> 'Identity':
        resp = cls._client.post(cls._endpoint, json=dict(metadata=metadata))
        return cls(**resp)
