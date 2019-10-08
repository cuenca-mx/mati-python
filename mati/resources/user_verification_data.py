import io
from dataclasses import dataclass
from typing import ClassVar, Union

from ..types import PageType, ValidationInputType, ValidationType
from .base import Resource


@dataclass
class UserValidationData(Resource):
    """
    Based on: https://docs.getmati.com/#step-3-upload-user-verification-data
    """

    _endpoint: ClassVar[str] = '/v2/identities/{identity_id}/send-input'

    @classmethod
    def create(
        cls,
        identity_id: str,
        filename: str,
        content: io.RawIOBase,
        input_type: Union[str, ValidationInputType],
        validation_type: Union[str, ValidationType],
        country: str,  # alpha-2 code: https://www.iban.com/country-codes
        region: str = '',  # 2-digit US State code (if applicable)
        group: int = 0,
        page: Union[str, PageType] = PageType.front,
    ) -> 'UserValidationData':
        endpoint = cls._endpoint.format(identity_id=identity_id)
        data = dict(
            filename=filename,
            inputType=input_type,
            group=group,
            type=validation_type,
            country=country,
            region=region,
            page=page,
        )
        files = [(filename, content)]
        resp = cls._client.post(endpoint, json=[data], files=files)
        return resp
