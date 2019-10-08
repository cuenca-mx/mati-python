from typing import ClassVar

import iso8601


class Resource:
    _client = ClassVar['mati.Client']
    _endpoint = ClassVar[str]

    def __post_init__(self):
        for attr, value in self.__dict__.items():
            if attr.startswith('date'):
                setattr(self, attr, iso8601.parse_date(value))
