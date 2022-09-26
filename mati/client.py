import os
from typing import Any, ClassVar, Dict, Optional, Tuple, Union

from requests import Response, Session

from .resources import AccessToken, Resource, UserValidationData, Verification
from .version import __version__ as client_version

API_URL = 'https://api.getmati.com'


class Client:

    base_url: ClassVar[str] = API_URL
    basic_auth_creds: Tuple[str, str]
    bearer_token: Optional[AccessToken]
    headers: Dict[str, str]
    session: Session

    # resources
    access_tokens: ClassVar = AccessToken
    user_validation_data: ClassVar = UserValidationData
    verifications: ClassVar = Verification

    def __init__(
        self, api_key: Optional[str] = None, secret_key: Optional[str] = None
    ):
        self.session = Session()
        self.headers = {'User-Agent': f'mati-python/{client_version}'}
        api_key = api_key or os.environ['MATI_API_KEY']
        secret_key = secret_key or os.environ['MATI_SECRET_KEY']
        self.basic_auth_creds = (api_key, secret_key)
        self.bearer_token = None
        Resource._client = self

    def get_valid_bearer_token(self) -> Optional[AccessToken]:
        expired_or_none = (
            self.bearer_token.expired if self.bearer_token else True
        )
        if expired_or_none:  # renew token
            self.bearer_token = self.access_tokens.create(client=self)
        return self.bearer_token

    def get(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self.request('get', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self.request('post', endpoint, **kwargs)

    def request(
        self,
        method: str,
        endpoint: str,
        auth: Union[str, AccessToken, None] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        url = self.base_url + endpoint
        auth = auth or self.get_valid_bearer_token()
        headers = {**self.headers, **dict(Authorization=str(auth))}
        response = self.session.request(method, url, headers=headers, **kwargs)
        self._check_response(response)
        return response.json()

    @staticmethod
    def _check_response(response: Response) -> None:
        if response.ok:
            return
        response.raise_for_status()
