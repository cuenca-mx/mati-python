from dataclasses import dataclass, fields
from typing import ClassVar, Dict, Optional, Union

import iso8601


@dataclass
class Resource:
    _client: ClassVar['mati.Client']  # type: ignore
    _endpoint: ClassVar[str]
    _token_score: ClassVar[Optional[str]] = None

    # purely for MyPy
    def __init__(self, **_):  # pragma: no cover
        ...

    def __post_init__(self) -> None:
        for attr, value in self.__dict__.items():
            if attr.startswith('date'):
                setattr(self, attr, iso8601.parse_date(value))

    @classmethod
    def _from_dict(cls, obj_dict: Dict[str, Union[str, int]]) -> 'Resource':
        cls._filter_excess_fields(obj_dict)
        return cls(**obj_dict)

    @classmethod
    def _filter_excess_fields(cls, obj_dict):
        """
        dataclasses don't allow __init__ to be called with excess fields. This
        method allows the API to add fields in the response body without
        breaking the client
        """
        excess = set(obj_dict.keys()) - {f.name for f in fields(cls)}
        for f in excess:
            del obj_dict[f]
