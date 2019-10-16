from typing import ClassVar, Optional

import iso8601


class Resource:
    _client: ClassVar['mati.Client']  # type: ignore
    _endpoint: ClassVar[str]
    _token_score: ClassVar[Optional[str]] = None

    def __post_init__(self) -> None:
        for attr, value in self.__dict__.items():
            if attr.startswith('date'):
                setattr(self, attr, iso8601.parse_date(value))
