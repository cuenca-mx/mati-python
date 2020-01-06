import json
from typing import Any, BinaryIO, ClassVar, Dict, List, Tuple

from mati.types import UserValidationFile, ValidationInputType

from .base import Resource


def get_file_type(file: UserValidationFile) -> str:
    input_type = file.input_type
    if input_type == 'selfie-video':
        file_type = 'video'
    elif input_type == 'selfie-photo':
        file_type = 'selfie'
    else:
        file_type = 'document'
    return file_type


class UserValidationData(Resource):
    """
    Based on: https://docs.getmati.com/#step-3-upload-user-verification-data
    """

    _endpoint: ClassVar[str] = '/v2/identities/{identity_id}/send-input'

    @staticmethod
    def _append_file(
        files_metadata: List[Dict[str, Any]], file: UserValidationFile
    ):
        if file.input_type == ValidationInputType.document_photo:
            files_metadata.append(
                dict(
                    inputType=file.input_type,
                    group=file.group,
                    data=dict(
                        type=file.validation_type,
                        country=file.country,
                        page=file.page,
                        filename=file.filename,
                        region=file.region,
                    ),
                )
            )
        else:
            files_metadata.append(
                dict(
                    inputType=file.input_type,
                    data=dict(filename=file.filename),
                )
            )

    @classmethod
    def upload(
        cls,
        identity_id: str,
        user_validation_files: List[UserValidationFile],
        client=None,
    ) -> List[Dict[str, Any]]:
        endpoint = cls._endpoint.format(identity_id=identity_id)
        files_metadata: List[Dict[str, Any]] = []
        files_with_types: List[Tuple[str, BinaryIO]] = []
        for file in user_validation_files:
            cls._append_file(files_metadata, file)
            files_with_types.append((get_file_type(file), file.content))
        resp = client.post(
            endpoint,
            data=dict(inputs=json.dumps(files_metadata)),
            files=files_with_types,
        )
        return resp
