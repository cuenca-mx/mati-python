import json
from json import JSONDecodeError

import pytest

from mati import Client


def scrub_access_token(response: dict) -> dict:
    try:
        resp = json.loads(response['body']['string'])
    except JSONDecodeError:
        pass
    else:
        if 'access_token' in resp:
            resp['access_token'] = 'ACCESS_TOKEN'
            user = resp['payload']['user']
            user['_id'] = 'ID'
            user['firstName'] = 'FIRST_NAME'
            user['lastName'] = 'LAST_NAME'
            resp['payload']['user'] = user
            response['body']['string'] = json.dumps(resp).encode('utf-8')
    return response


@pytest.fixture(scope='module')
def vcr_config() -> dict:
    config = dict()
    config['filter_headers'] = [('Authorization', None)]
    config['before_record_response'] = scrub_access_token
    return config


@pytest.fixture
def client():
    # using credentials from env
    yield Client()
