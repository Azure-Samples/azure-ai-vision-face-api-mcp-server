import os
from typing import Annotated

from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import (
    FaceAttributeType,
    FaceDetectionModel,
    FaceRecognitionModel,
)
from azure.core.credentials import AzureKeyCredential
from pydantic import Field

from .utils._enums import AzureFaceAttribConfig


def get_face_dect(
    file_path: Annotated[str, Field(description=AzureFaceAttribConfig.ARGS_FILE_PATH)],
    is_url: Annotated[bool, Field(description=AzureFaceAttribConfig.ARGS_IS_URL)] = False,
    return_HEAD_POSE: Annotated[bool, Field(description=AzureFaceAttribConfig.ARGS_RETURN_HEAD_POSE)] = False,
    return_GLASSES: Annotated[bool, Field(description=AzureFaceAttribConfig.ARGS_RETURN_GLASSES)] = False,
    return_OCCLUSION: Annotated[bool, Field(description=AzureFaceAttribConfig.ARGS_RETURN_OCCLUSION)] = False,
    return_BLUR: Annotated[bool, Field(description=AzureFaceAttribConfig.ARGS_RETURN_BLUR)] = False,
    return_EXPOSURE: Annotated[bool, Field(description=AzureFaceAttribConfig.ARGS_RETURN_EXPOSURE)] = False,
    return_MASK: Annotated[bool, Field(description=AzureFaceAttribConfig.ARGS_RETURN_MASK)] = False,
    return_QUALITY_FOR_RECOGNITION: Annotated[bool, Field(description=AzureFaceAttribConfig.ARGS_RETURN_QUALITY_FOR_RECOGNITION)] = False,
    return_AGE: Annotated[bool, Field(description=AzureFaceAttribConfig.ARGS_RETURN_AGE)] = False,
    return_landmarks: Annotated[bool, Field(description=AzureFaceAttribConfig.ARGS_RETURN_LANDMARKS)] = False,
):
    if file_path is None:
        return "The face api did not receive any image. Please provide an image."
    ENDPOINT = os.getenv("FACE_ENDPOINT")
    KEY = os.getenv("FACE_API_KEY")
    face_atributes = []
    if return_HEAD_POSE is True:
        face_atributes.append(FaceAttributeType.HEAD_POSE)
    if return_GLASSES is True:
        face_atributes.append(FaceAttributeType.GLASSES)
    if return_OCCLUSION is True:
        face_atributes.append(FaceAttributeType.OCCLUSION)
    if return_BLUR is True:
        face_atributes.append(FaceAttributeType.BLUR)
    if return_EXPOSURE is True:
        face_atributes.append(FaceAttributeType.EXPOSURE)
    if return_MASK is True:
        face_atributes.append(FaceAttributeType.MASK)
    if return_QUALITY_FOR_RECOGNITION is True:
        face_atributes.append(FaceAttributeType.QUALITY_FOR_RECOGNITION)
    if return_AGE is True:
        face_atributes.append(FaceAttributeType.AGE)
    with FaceClient(
        endpoint=ENDPOINT, credential=AzureKeyCredential(KEY),
        headers = {"X-MS-AZSDK-Telemetry": "sample=mcp-face-detect-attr"}
    ) as face_client:
        if is_url is True:
            detected_faces = face_client.detect_from_url(
                url=file_path,
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=True,
                return_face_landmarks=return_landmarks,
                return_face_attributes=face_atributes
            )
        else:
            if os.path.exists(file_path) is False:
                return "The client provided image does not exist in its path."
            
            detected_faces = face_client.detect(
                image_content=open(file_path, "rb"),
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=True,
                return_face_landmarks=return_landmarks,
                return_face_attributes=face_atributes
            )
    results = []
    for face in detected_faces:
        result = f"""
        Azure AI Face API Dection Results: {face}
        """
        results.append(result)
    return "\n---\n".join(results)