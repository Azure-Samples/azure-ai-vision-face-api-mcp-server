import os
from typing import Annotated
import json

from azure.ai.vision.face import FaceAdministrationClient, FaceClient
from azure.ai.vision.face.models import (
    FaceAttributeTypeRecognition04,
    FaceDetectionModel,
    FaceRecognitionModel,
    QualityForRecognition,
)
from azure.core.credentials import AzureKeyCredential
from pydantic import Field

from .utils._enums import EnrollFaceToLPGConfig


def enroll_face_to_group(
    file_path_list: Annotated[
        list, Field(description=EnrollFaceToLPGConfig.ARGS_FILE_PATH_LIST)
    ],
    person_name: Annotated[
        str, Field(description=EnrollFaceToLPGConfig.ARGS_PERSON_NAME)
    ],
    group_uuid: Annotated[
        str, Field(description=EnrollFaceToLPGConfig.ARGS_GROUP_UUID)
    ],
    is_url: Annotated[
        bool, Field(description=EnrollFaceToLPGConfig.ARGS_IS_URL)
    ] = False,
    check_quality: Annotated[
        bool, Field(description=EnrollFaceToLPGConfig.ARGS_CHECK_QUALITY)
    ] = True,
):
    ENDPOINT = os.getenv("AZURE_FACE_ENDPOINT")
    KEY = os.getenv("AZURE_FACE_API_KEY")
    UUID = group_uuid
    output_list = []
    with (
        FaceAdministrationClient(
            endpoint=ENDPOINT,
            credential=AzureKeyCredential(KEY),
            headers={"X-MS-AZSDK-Telemetry": "sample=mcp-face-reco-enroll"},
        ) as face_admin_client,
        FaceClient(
            endpoint=ENDPOINT,
            credential=AzureKeyCredential(KEY),
            headers={"X-MS-AZSDK-Telemetry": "sample=mcp-face-reco-detect-for-enroll"},
        ) as face_client,
    ):
        # add person name to the large person group
        new_person = face_admin_client.large_person_group.create_person(
            large_person_group_id=UUID,
            name=person_name,
        )
        output_list.append(
            f"Create the person name: {person_name}"
            f" with person id: {new_person.person_id}"
            f" in the large person group with group UUID: {UUID}"
        )
        for file_path in file_path_list:
            if is_url is True:
                detected_faces = face_client.detect_from_url(
                    url=file_path,
                    detection_model=FaceDetectionModel.DETECTION03,
                    recognition_model=FaceRecognitionModel.RECOGNITION04,
                    return_face_id=True,
                    return_face_attributes=[
                        FaceAttributeTypeRecognition04.QUALITY_FOR_RECOGNITION
                    ],
                )
            else:
                if not os.path.exists(file_path):
                    output_list.append(
                        f"Image file: {file_path} does not exist. Ignoring this image."
                    )
                    continue
                detected_faces = face_client.detect(
                    image_content=open(file_path, "rb"),
                    detection_model=FaceDetectionModel.DETECTION03,
                    recognition_model=FaceRecognitionModel.RECOGNITION04,
                    return_face_id=True,
                    return_face_attributes=[
                        FaceAttributeTypeRecognition04.QUALITY_FOR_RECOGNITION
                    ],
                )
            detected_face = None
            if len(detected_faces) < 1:
                output_list.append(
                    f"Image file: {file_path} does not contain any faces. "
                    "Ignoring this image."
                )
                continue
            if check_quality is False:
                filtered_faces = detected_faces
            else:
                filtered_faces = [
                    face
                    for face in detected_faces
                    if face.face_attributes.quality_for_recognition
                    == QualityForRecognition.HIGH
                ]
            if len(filtered_faces) < 1:
                output_list.append(
                    f"Image file: {file_path} contains {len(detected_faces)} "
                    "faces but no faces with high quality for recognition. "
                    "Ignoring this image."
                )
                continue
            elif len(filtered_faces) == 1:
                detected_face = filtered_faces[0]
                output_list.append(
                    f"Image file: {file_path} contains 1 face for recognition."
                    f" Face ID: {detected_face.face_id} "
                    f"(bounding box: {detected_face.face_rectangle})."
                )
            else:
                detected_faces_area_list = [
                    face.face_rectangle.width * face.face_rectangle.height
                    for face in filtered_faces
                ]
                largest_face_index = detected_faces_area_list.index(
                    max(detected_faces_area_list)
                )
                detected_face = filtered_faces[largest_face_index]
                output_list.append(
                    f"Image file: {file_path} contains more than 1 face for recognition. Selecting the largest face."
                    f" Face ID: {detected_face.face_id} "
                    f"(bounding box: {detected_face.face_rectangle})."
                )
            if is_url:
                persisted_face = face_admin_client.large_person_group.add_face_from_url(
                    large_person_group_id=UUID,
                    person_id=new_person.person_id,
                    url=file_path,
                    target_face=[
                        detected_face.face_rectangle.left,
                        detected_face.face_rectangle.top,
                        detected_face.face_rectangle.width,
                        detected_face.face_rectangle.height,
                    ],
                    detection_model=FaceDetectionModel.DETECTION03,
                    user_data=json.dumps({"file_path": file_path.split("?")[0]}),
                )
            else:
                persisted_face = face_admin_client.large_person_group.add_face(
                    large_person_group_id=UUID,
                    person_id=new_person.person_id,
                    image_content=open(file_path, "rb"),
                    target_face=[
                        detected_face.face_rectangle.left,
                        detected_face.face_rectangle.top,
                        detected_face.face_rectangle.width,
                        detected_face.face_rectangle.height,
                    ],
                    detection_model=FaceDetectionModel.DETECTION03,
                    user_data=json.dumps({"file_path": file_path}),
                )
            output_list.append(
                f"Add image file: {file_path} to person name: {person_name} "
                f"with person id: {new_person.person_id} in the group with "
                f"group UUID {UUID}. Persisted face ID: {persisted_face.persisted_face_id}"
            )
            poller = face_admin_client.large_person_group.begin_train(
                large_person_group_id=UUID,
                polling_interval=5,
            )
            poller.wait()
    return "\n---\n".join(output_list)
