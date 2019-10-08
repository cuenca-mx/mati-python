from dataclasses import dataclass
from datetime import datetime


@dataclass
class Identity:
    _id: str
    metadata: dict
    dateCreated: datetime
    dateUpdated: datetime
    status: str
    user: str
    alive: None

    def to_request(self) -> dict:
        return dict(metadata=self.metadata)
