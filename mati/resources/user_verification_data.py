import io
import json

from io import BufferedReader

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
            inputType=input_type,
            group=group,
            data=dict(
                type=validation_type,
                country=country,
                page=page.value,
                filename=filename
            )
        )
        files = cls.files(input_type, content)
        resp = cls._client.post(endpoint, data={'inputs': json.dumps([data])}, files=files)
        return resp

    @staticmethod
    def files(input_type: str, content: BufferedReader) -> dict:
        files = dict(document=content)
        if input_type == 'selfie-video':
            dict(video=content)
            files = [('video', content)]
        elif input_type == 'selfie_photo':
            dict(selfie=content)
        return files


