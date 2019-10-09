import os
from typing import ClassVar, Optional, Union

from requests import Response, Session

from .resources import AccessToken, Identity, Resource, UserValidationData

API_URL = 'https://api.getmati.com'


class Client:

    base_url: ClassVar[str] = API_URL
    session: Session
    basic_auth_creds: tuple
    bearer_token: Optional[AccessToken]

    # resources
    access_tokens: ClassVar = AccessToken
    identities: ClassVar = Identity
    user_validation_data: ClassVar = UserValidationData

    def __init__(
        self, api_key: Optional[str] = None, secret_key: Optional[str] = None
    ):
        self.session = Session()
        api_key = api_key or os.environ['MATI_API_KEY']
        secret_key = secret_key or os.environ['MATI_SECRET_KEY']
        self.basic_auth_creds = (api_key, secret_key)
        self.bearer_token = None
        Resource._client = self

    def get_valid_bearer_token(self) -> AccessToken:
        if self.bearer_token is None or self.bearer_token.expired:
            self.bearer_token = self.access_tokens.create()  # renew token
        return self.bearer_token

    def get(self, endpoint: str, **kwargs) -> dict:
        return self.request('get', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> dict:
        return self.request('post', endpoint, **kwargs)

    def request(
        self,
        method: str,
        endpoint: str,
        auth: Union[str, AccessToken, None] = None,
        **kwargs,
    ) -> dict:
        url = self.base_url + endpoint
        auth = auth or self.get_valid_bearer_token()
        headers = dict(Authorization=str(auth))
        response = self.session.request(method, url, headers=headers, **kwargs)
        self._check_response(response)
        return response.json()

    @staticmethod
    def _check_response(response: Response):
        if response.ok:
            return
        response.raise_for_status()
