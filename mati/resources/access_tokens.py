import datetime as dt
from dataclasses import dataclass
from typing import ClassVar, Optional

from ..auth import basic_auth_str, bearer_auth_str
from .base import Resource


@dataclass
class AccessToken(Resource):
    """
    Based on: https://docs.getmati.com/#step-1-authentication
    """

    _endpoint: ClassVar[str] = '/oauth'

    user_id: str
    token: str
    expires_at: dt.datetime
    score: Optional[str]

    @classmethod
    def create(cls, score: Optional[str] = None) -> 'AccessToken':
        data = dict(grant_type='client_credentials')
        endpoint = cls._endpoint
        if score:
            data['score'] = score
            endpoint += '/token'
        resp = cls._client.post(
            cls._endpoint,
            data=data,
            auth=basic_auth_str(*cls._client.basic_auth_creds),
        )
        expires_at = dt.datetime.now() + dt.timedelta(
            seconds=resp['expiresIn']
        )
        return cls(
            user_id=resp['payload']['user']['_id'],
            token=resp['access_token'],
            expires_at=expires_at,
            score=score,
        )

    def __str__(self) -> str:
        return bearer_auth_str(self.token)

    @property
    def expired(self) -> bool:
        return self.expires_at < dt.datetime.now()
