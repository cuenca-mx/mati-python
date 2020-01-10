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

## Create Identity

```python
from mati import Client

client = Client()
georg = client.identities.create(
    name='Georg Wilhelm Friedrich Hegel',
    occupation='Philosopher',
    dob='1770-08-27'
)
```
