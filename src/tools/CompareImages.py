from mcp.server.fastmcp import FastMCP

import os
import base64

from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import FaceDetectionModel, FaceRecognitionModel
import cv2
from openai import AzureOpenAI
from typing import Annotated, Literal
from pydantic import Field
from .utils._enums import CompareImagesConfig


def compare_source_image_to_target_image(
    source_image: Annotated[str, Field(description=CompareImagesConfig.ARGS_SOURCE_IMAGE)],
    target_image: Annotated[str, Field(description=CompareImagesConfig.ARGS_TARGET_IMAGE)],
    comparison_mode: Annotated[
        Literal["largest_face", "most_similar", "exhaustive"],
        Field(description=CompareImagesConfig.ARGS_COMPARISON_MODE)
    ],
    is_source_image_url: Annotated[bool, Field(description=CompareImagesConfig.ARGS_IS_SOURCE_IMAGE_URL)] = False,
    is_target_image_url: Annotated[bool, Field(description=CompareImagesConfig.ARGS_IS_TARGET_IMAGE_URL)] = False,
    identical_threshold: Annotated[float, Field(description=CompareImagesConfig.ARGS_THRESHOLD, ge=0.0, le=1.0)] = 0.5
):
    ENDPOINT = os.getenv("FACE_ENDPOINT")
    KEY = os.getenv("FACE_API_KEY")
    output_list = []
    with FaceClient(
        endpoint=ENDPOINT, 
        credential=AzureKeyCredential(KEY), 
        headers = {"X-MS-AZSDK-Telemetry": "sample=mcp-face-reco-compare-two-images"}
    ) as face_client:
        # Detect faces in source image
        if is_source_image_url is True:
            detected_faces_source = face_client.detect_from_url(
                url=source_image,
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=True,
            )
        else:
            if not os.path.exists(source_image):
                return f"Image file: {source_image} does not exist."
            
            detected_faces_source = face_client.detect(
                image_content=open(source_image, "rb"),
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=True,
            )
        if len(detected_faces_source) < 1:
            return (
                f"Image file: {source_image} does not contain any "
                "detectable faces. No comparison can be performed."
            )
        
        # Detect faces in target image
        if is_target_image_url is True:
            detected_faces_target = face_client.detect_from_url(
                url=target_image,
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=True,
            )
        else:
            if not os.path.exists(target_image):
                return f"Image file: {target_image} does not exist."
            
            detected_faces_target = face_client.detect(
                image_content=open(target_image, "rb"),
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=True,
            )
        if len(detected_faces_target) < 1:
            return (
                f"Image file: {target_image} does not contain any "
                "detectable faces. No comparison can be performed."
            )
        if comparison_mode == "exhaustive":
            output_list.append(
                "Exhaustive comparison is requested. Comparing all detected "
                f"faces in the image file: {source_image} with all detected faces in the "
                f"image file: {target_image}"
            )
            for detected_face_source in detected_faces_source:
                similar_faces = face_client.find_similar({
                    "faceId": detected_face_source.face_id,
                    "faceIds": [face.face_id for face in detected_faces_target],
                    "maxNumOfCandidatesReturned": len(detected_faces_target),
                    "mode": "matchFace",
                })
                for similar_face in similar_faces:
                    output_list.append(
                        f"Face ID: {detected_face_source.face_id}, "
                        f"Face ID: {similar_face.face_id}, "
                        f"Verification result: "
                        f"{similar_face.confidence >= identical_threshold}, "
                        f"Confidence: {similar_face.confidence}"
                    )
        elif comparison_mode == "most_similar":
            output_list.append(
                "Most similar comparison is requested. For each face in the "
                f"image file: {source_image}, the most similar face from the image file: {target_image} "
                "will be determined."
            )
            for detected_face_source in detected_faces_source:
                similar_faces = face_client.find_similar({
                    "faceId": detected_face_source.face_id,
                    "faceIds": [face.face_id for face in detected_faces_target],
                    "maxNumOfCandidatesReturned": 1,
                    "mode": "matchPerson",
                })
                if len(similar_faces) > 0:
                    output_list.append(
                        f"Face ID: {detected_face_source.face_id}, "
                        f"with most similar Face ID: {similar_faces[0].face_id}, "
                        f"Verification result: "
                        f"{similar_faces[0].confidence >= identical_threshold}, "
                        f"Confidence: {similar_faces[0].confidence}"
                    )
                else:
                    output_list.append(
                        f"Face ID: {detected_face_source.face_id} did not "
                        "find a similar face in another image."
                    )
        else:
            output_list.append(
                "Largest face comparison is requested. Only comparing the "
                "largest detected face in each image."
            )
            # select the largest face in source image
            detected_faces_area_list_source = [
                face.face_rectangle.width * face.face_rectangle.height
                for face in detected_faces_source
            ]
            largest_face_index_source = detected_faces_area_list_source.index(
                max(detected_faces_area_list_source)
            )
            detected_face_source = detected_faces_source[largest_face_index_source]
            face_id_source = detected_face_source.face_id
            output_list.append(
                f"Image file: {source_image} contains "
                f"{len(detected_faces_source)} face(s). Using the largest face "
                f"with Face ID: {face_id_source} for comparison."
            )
            # select the largest face in target image
            detected_faces_area_list_target = [
                face.face_rectangle.width * face.face_rectangle.height
                for face in detected_faces_target
            ]
            largest_face_index_target = detected_faces_area_list_target.index(
                max(detected_faces_area_list_target)
            )
            detected_face_target = detected_faces_target[largest_face_index_target]
            face_id_target = detected_face_target.face_id
            output_list.append(
                f"Image file: {target_image} contains "
                f"{len(detected_faces_target)} face(s). Using the largest face "
                f"with Face ID: {face_id_target} for comparison."
            )
            # Compare the two faces
            verify_result = face_client.verify_face_to_face(
                face_id1=face_id_source,
                face_id2=face_id_target,
            )
            output_list.append(
                f"Face ID: {face_id_source}, "
                f"Face ID: {face_id_target}, "
                f"Verification result: "
                f"{verify_result.confidence >= identical_threshold}, "
                f"Confidence: {verify_result.confidence}"
            )
        return "\n---\n".join(output_list)