import os
from typing import Annotated

from pydantic import Field
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import FaceDetectionModel, FaceRecognitionModel
from azure.core.credentials import AzureKeyCredential

from .utils._enums import IdentifyFaceInLPGConfig


def identify_face_from_group(
    file_path: Annotated[str, Field(description=IdentifyFaceInLPGConfig.ARGS_FILE_PATH)], 
    group_uuid: Annotated[str, Field(description=IdentifyFaceInLPGConfig.ARGS_GROUP_UUID)],
    is_url: Annotated[bool, Field(description=IdentifyFaceInLPGConfig.ARGS_IS_URL)] = False
):
    ENDPOINT = os.getenv("AZURE_FACE_ENDPOINT")
    KEY = os.getenv("AZURE_FACE_API_KEY")
    output_list = []
    with FaceClient(
        endpoint=ENDPOINT, credential=AzureKeyCredential(KEY), 
        headers = {"X-MS-AZSDK-Telemetry": "sample=mcp-face-reco-identify"}
    ) as face_client:
        if is_url is True:
            faces = face_client.detect_from_url(
                url=file_path,
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=True,
            )
        else:
            if not os.path.exists(file_path):
                return f"Image file: {file_path} does not exist."
            
            faces = face_client.detect(
                image_content=open(file_path, "rb"),
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=True,
            )
        if len(faces) == 0:
            return f"No face detected in the provided image file: {file_path}"
        else:
            output_list.append(
                f"Detected {len(faces)} face(s) in the provided image file: "
                f"{file_path}"
            )
        face_ids = [face.face_id for face in faces]
        face_id_to_bbox = {face.face_id: face.face_rectangle for face in faces}
        identify_results = face_client.identify_from_large_person_group(
            face_ids=face_ids,
            large_person_group_id=group_uuid,
        )
        output_list = []
        for idx, identify_result in enumerate(identify_results):
            face_id = face_ids[idx]
            bbox = face_id_to_bbox.get(face_id, None)
            if identify_result.candidates:
                output_list.append(
                    f"Face ID {face_id} (bounding box: {bbox}) in the image was identified as "
                    f"person ID: {identify_result.candidates[0]['personId']} "
                    f"with confidence: {identify_result.candidates[0]['confidence']} "
                    f"in the group with UUID: {group_uuid}"
                )
            else:
                output_list.append(
                    f"Face ID {face_id} (bounding box: {bbox}) in the image could not be "
                    f"identified in the group with UUID: {group_uuid}"
                )
    return "\n---\n".join(output_list)