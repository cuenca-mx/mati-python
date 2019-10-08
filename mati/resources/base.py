from typing import ClassVar


class Resource:
    _client = ClassVar['mati.Client']
    _endpoint = ClassVar[str]
