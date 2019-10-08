import datetime as dt
import os
from typing import ClassVar, Optional

from requests import Response, Session

from .resources import AccessToken, Resource

API_URL = 'https://api.getmati.com'


class Client:

    base_url: ClassVar[str] = API_URL
    session: Session
    basic_auth_creds: tuple
    bearer_token: AccessToken
    headers: dict

    # resources
    access_tokens = AccessToken

    def __init__(
        self, api_key: Optional[str] = None, secret_key: Optional[str] = None
    ):
        self.session = Session()
        api_key = api_key or os.environ['MATI_API_KEY']
        secret_key = secret_key or os.environ['MATI_SECRET_KEY']
        self.basic_auth_creds = (api_key, secret_key)
        self.bearer_token = AccessToken(token='', expires_at=dt.datetime.now())
        Resource._client = self

    def renew_access_token(self):
        self.bearer_token = self.access_tokens.create()

    def post(self, endpoint: str, **kwargs):
        return self.request('post', endpoint, **kwargs)

    def request(
        self, method: str, endpoint: str, auth: Optional[str] = None, **kwargs
    ) -> dict:
        url = self.base_url + endpoint
        if auth is None:
            if self.bearer_token.expired:
                self.renew_access_token()
            auth = str(self.bearer_token)
        headers = dict(Authorization=auth)
        response = self.session.request(method, url, headers=headers, **kwargs)
        self._check_response(response)
        return response.json()

    @staticmethod
    def _check_response(response: Response):
        if response.ok:
            return
        response.raise_for_status()
