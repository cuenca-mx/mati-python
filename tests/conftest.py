import json
from json import JSONDecodeError
from typing import Generator

import pytest

from mati import Client

VERIFICATION_RESP = {
    'expired': False,
    'identity': {'status': 'verified'},
    'flow': {'id': '5e9576d9ac2c70001ca9f092', 'name': 'Default flow'},
    'steps': [],
    'documents': [
        {
            'country': 'MX',
            'region': '',
            'photos': [
                'https://media.getmati.com/media/xxx',
                'https://media.getmati.com/media/yyy',
            ],
            'steps': [
                {'error': None, 'status': 200, 'id': 'template-matching'},
                {
                    'error': None,
                    'status': 200,
                    'id': 'mexican-curp-validation',
                    'data': {
                        'curp': 'CURP',
                        'fullName': 'LAST FIRST',
                        'birthDate': '01/01/1980',
                        'gender': 'HOMBRE',
                        'nationality': 'MEXICO',
                        'surname': 'LAST',
                        'secondSurname': '',
                        'name': 'FIRST',
                    },
                },
                {
                    'error': None,
                    'status': 200,
                    'id': 'document-reading',
                    'data': {
                        'fullName': {
                            'value': 'FIRST LAST',
                            'label': 'Name',
                            'sensitive': True,
                        },
                        'documentNumber': {
                            'value': '111',
                            'label': 'Document Number',
                        },
                        'dateOfBirth': {
                            'value': '1980-01-01',
                            'label': 'Day of Birth',
                            'format': 'date',
                        },
                        'expirationDate': {
                            'value': '2030-12-31',
                            'label': 'Date of Expiration',
                            'format': 'date',
                        },
                        'curp': {'value': 'CURP', 'label': 'CURP'},
                        'address': {
                            'value': 'Varsovia 36, 06600 CDMX',
                            'label': 'Address',
                        },
                        'emissionDate': {
                            'value': '2010-01-01',
                            'label': 'Emission Date',
                            'format': 'date',
                        },
                    },
                },
                {'error': None, 'status': 200, 'id': 'alteration-detection'},
                {'error': None, 'status': 200, 'id': 'watchlists'},
            ],
            'type': 'national-id',
            'fields': {
                'fullName': {
                    'value': 'FIRST LAST',
                    'label': 'Name',
                    'sensitive': True,
                },
                'documentNumber': {'value': '111', 'label': 'Document Number'},
                'dateOfBirth': {
                    'value': '1980-01-01',
                    'label': 'Day of Birth',
                    'format': 'date',
                },
                'expirationDate': {
                    'value': '2030-12-31',
                    'label': 'Date of Expiration',
                    'format': 'date',
                },
                'curp': {'value': 'CURP', 'label': 'CURP'},
                'address': {
                    'value': 'Varsovia 36, 06600 CDMX',
                    'label': 'Address',
                },
                'emissionDate': {
                    'value': '2010-01-01',
                    'label': 'Emission Date',
                    'format': 'date',
                },
            },
        }
    ],
    'hasProblem': False,
    'computed': {'age': {'data': 100}},
    'id': '5d9fb1f5bfbfac001a349bfb',
    'metadata': {'name': 'First Last', 'dob': '1980-01-01'},
}


def scrub_sensitive_info(response: dict) -> dict:
    response = scrub_access_token(response)
    response = swap_verification_body(response)
    return response


def scrub_access_token(response: dict) -> dict:
    try:
        resp = json.loads(response['body']['string'])
    except (JSONDecodeError, KeyError):
        pass
    else:
        if 'access_token' in resp:
            resp['access_token'] = 'ACCESS_TOKEN'
            try:
                user = resp['payload']['user']
            except KeyError:
                pass
            else:
                user['_id'] = 'ID'
                user['firstName'] = 'FIRST_NAME'
                user['lastName'] = 'LAST_NAME'
                resp['payload']['user'] = user
            response['body']['string'] = json.dumps(resp).encode('utf-8')
    return response


def swap_verification_body(response: dict) -> dict:
    if b'curp' not in response['body']['string']:
        return response
    response['body']['string'] = json.dumps(VERIFICATION_RESP).encode('utf-8')
    return response


@pytest.fixture(scope='module')
def vcr_config() -> dict:
    config = dict()
    config['filter_headers'] = [('Authorization', None)]
    config['before_record_response'] = scrub_sensitive_info  # type: ignore
    return config


@pytest.fixture
def client() -> Generator:
    yield Client('api_key', 'secret_key')


@pytest.fixture
def identity(client: Client) -> Generator:
    yield client.identities.create(
        client=client,
        nombres='Georg Wilhelm',
        primer_apellido='Friedrich',
        segundo_apellido='Hegel',
        dob='1770-08-27',
    )
