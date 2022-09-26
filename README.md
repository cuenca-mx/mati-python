# mati-python
[![Build Status](https://travis-ci.com/cuenca-mx/mati-python.svg?branch=master)](https://travis-ci.com/cuenca-mx/mati-python)
[![Coverage Status](https://coveralls.io/repos/github/cuenca-mx/mati-python/badge.svg?branch=master)](https://coveralls.io/github/cuenca-mx/mati-python?branch=master)
[![PyPI](https://img.shields.io/pypi/v/mati.svg)](https://pypi.org/project/mati/)

[Mati](https://mati.io) Python3.6+ client library


## Install

```
pip install mati
```

## Testing

```
make venv
source venv/bin/activate
make test
```

## Create Verification

```python
from mati import Client

client = Client('api_key', 'secret_key')
verification = client.verifications.create(
    'some_flow_id',
    company_id='some_id',
)
```

## Upload documents
```python
from mati.types import (
    PageType,
    UserValidationFile,
    ValidationInputType,
    ValidationType,
)

# Load documents
front = open('ine_front.jpg', 'rb')
back = open('ine_back.jpg', 'rb')
live = open('liveness.mp4', 'rb')

# Create document with metadata
user_validation_file = UserValidationFile(
    filename='ine_front.jpg',
    content=front,
    input_type=ValidationInputType.document_photo,
    validation_type=ValidationType.national_id,
    country='MX',
    group=0, #The group is important when create your metamap
)
user_validation_file_back = UserValidationFile(
    filename='ine_back.jpg',
    content=back,
    input_type=ValidationInputType.document_photo,
    validation_type=ValidationType.national_id,
    country='MX',
    page=PageType.back,
    group=0,
)
user_validation_live = UserValidationFile(
    filename='liveness.MOV',
    content=live,
    input_type=ValidationInputType.selfie_video,
    group=1,
)

# Send documentation for validation
resp = client.verifications.upload_validation_data(
    [
        user_validation_file,
        user_validation_file_back,
        user_validation_live,
    ],
    verification.identity,
)
```

## Verification status
Retrieve the verification when its complete
```python
verification = client.verifications.retrieve('verification_id')
```