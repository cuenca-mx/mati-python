import datetime as dt
from dataclasses import dataclass
from typing import ClassVar

from ..auth import basic_auth_str, bearer_auth_str
from .base import Resource


@dataclass
class AccessToken(Resource):
    """
    Based on: https://docs.getmati.com/#step-1-authentication
    """

    _endpoint: ClassVar[str] = '/oauth'

    token: str
    expires_at: dt.datetime

    @classmethod
    def create(cls) -> 'AccessToken':
        resp = cls._client.post(
            cls._endpoint,
            data=dict(grant_type='client_credentials'),
            auth=basic_auth_str(*cls._client.basic_auth_creds),
        )
        expires_at = dt.datetime.now() + dt.timedelta(
            seconds=resp['expiresIn']
        )
        return cls(token=resp['access_token'], expires_at=expires_at)

    def __str__(self) -> str:
        return bearer_auth_str(self.token)

    @property
    def expired(self) -> bool:
        return self.expires_at < dt.datetime.now()
