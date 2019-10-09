import io
import json
from dataclasses import dataclass
from typing import ClassVar, Union

from ..types import PageType, ValidationInputType, ValidationType
from .base import Resource


def file_with_type(input_type: str, content: io.BufferedReader) -> dict:
    if input_type == 'selfie-video':
        file_type = 'video'
    elif input_type == 'selfie-photo':
        file_type = 'selfie'
    else:
        file_type = 'document'
    return {file_type: content}


@dataclass
class UserValidationData(Resource):
    """
    Based on: https://docs.getmati.com/#step-3-upload-user-verification-data
    """

    _endpoint: ClassVar[str] = '/v2/identities/{identity_id}/send-input'

    @classmethod
    def upload(
        cls,
        identity_id: str,
        filename: str,
        content: io.BufferedReader,
        input_type: ValidationInputType,
        validation_type: Union[str, ValidationType],
        country: str,  # alpha-2 code: https://www.iban.com/country-codes
        region: str = '',  # 2-digit US State code (if applicable)
        group: int = 0,
        page: Union[str, PageType] = PageType.front,
    ) -> bool:
        endpoint = cls._endpoint.format(identity_id=identity_id)
        data = dict(
            inputType=input_type,
            group=group,
            data=dict(
                type=validation_type,
                country=country,
                page=page.value,
                filename=filename,
                region=region,
            ),
        )
        resp = cls._client.post(
            endpoint,
            data=dict(inputs=json.dumps([data])),
            files=file_with_type(input_type, content),
        )
        return resp[0]['result']
