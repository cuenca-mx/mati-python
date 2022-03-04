import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, Optional

from ..auth import basic_auth_str, bearer_auth_str
from .base import Resource

EXPIRATION_BUFFER = 30  # seconds. Gives us a buffer from expires_in


@dataclass
class AccessToken(Resource):
    """
    Based on: https://docs.getmati.com/#step-1-authentication
    """

    _endpoint: ClassVar[str] = '/oauth'

    token: str
    expires_at: dt.datetime
    user_id: Optional[str]

    @classmethod
    def create(cls, client=None) -> 'AccessToken':
        client = client or cls._client
        data = dict(grant_type='client_credentials')
        endpoint = cls._endpoint
        resp = client.post(
            endpoint,
            data=data,
            auth=basic_auth_str(*client.basic_auth_creds),
        )
        try:
            expires_in = resp['expiresIn']
        except KeyError:  # pragma: no cover
            expires_in = resp['expires_in']
        expires_at = dt.datetime.now() + dt.timedelta(
            seconds=expires_in - EXPIRATION_BUFFER
        )
        try:
            user_id = resp['payload']['user']['_id']
        except KeyError:  # pragma: no cover
            user_id = None
        return cls(
            user_id=user_id,
            token=resp['access_token'],
            expires_at=expires_at,
        )

    def __str__(self) -> str:
        return bearer_auth_str(self.token)

    @property
    def expired(self) -> bool:
        return self.expires_at < dt.datetime.now()
