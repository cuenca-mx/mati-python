import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta

import requests
from requests.auth import HTTPBasicAuth

from .resources import Document, Identity, ValidateRequest, Verification
from .types import ValidationInputType

API_URL = os.getenv('API_URL', 'https://api.getmati.com')
API_AUTH_URI = os.getenv('API_AUTH_URI', '/oauth')
API_IDENTITY_URI = os.getenv('API_IDENTITY_URI', '/v2/identities')


@dataclass
class Client:
    client_id: str
    client_secret: str
    token = None
    authenticated_at = None
    seconds = 0

    def _authenticate(self):
        # No está autenticada
        if not self.token or (
            self.authenticated_at + timedelta(seconds=self.seconds)
            < datetime.now()
        ):
            auth = HTTPBasicAuth(self.client_id, self.client_secret)
            response = requests.post(
                API_URL + API_AUTH_URI,
                auth=auth,
                data=dict(grant_type='client_credentials'),
            )
            if response.status_code == 200:
                self.token = response.json()['access_token']
                self.seconds = response.json()['expiresIn']
                self.authenticated_at = datetime.now()
            else:
                raise Exception

    def create_identity(self, person_id: str, person_name: str) -> Identity:
        self._authenticate()
        meta_data = {person_name, person_id}
        response = requests.post(
            API_URL + API_IDENTITY_URI,
            headers={'Authorization': 'Bearer ' + self.token},
            data=dict(metadata=meta_data),
        )
        if response.status_code == 200:
            identity = Identity(**response.json())
            return identity

    def validate_document(
        self, validation_request: ValidateRequest
    ) -> Verification:
        self._authenticate()
        response = dict(error='Invalid documents')
        if len(validation_request.documents) == 0:
            return Verification(**response)
        for document in validation_request.documents:

            request = self.get_validation_request(validation_request, document)
            documents = self._get_files_request(document)
            response = requests.post(
                API_URL
                + API_IDENTITY_URI
                + '/'
                + validation_request.identity_id
                + '/send-input',
                headers={'Authorization': 'Bearer ' + self.token},
                data={'inputs': json.dumps(request)},
                files=documents,
            )
            if response.status_code != 201:
                return Verification(**dict(error=response.json()))
        return Verification(**dict(result=response.json()))

    @staticmethod
    def _get_files_request(document: Document) -> dict:
        request = dict()
        request[document.validation_type.value] = document.stream
        return request

    @staticmethod
    def get_validation_request(request: ValidateRequest, document) -> dict:
        data = []
        if document.input_type == ValidationInputType.document_photo:
            data.append(
                dict(
                    inputType=document.input_type.value,
                    group=request.group,
                    data=dict(
                        type=document.document_type.value,
                        country=request.country,
                        page=document.page,
                        filename=document.file_name,
                    ),
                )
            )
        else:
            data.append(
                dict(
                    inputType=document.input_type.value,
                    data=dict(filename=document.file_name),
                )
            )
        return data
