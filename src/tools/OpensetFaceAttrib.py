import os
import base64

from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceAdministrationClient, FaceClient
from azure.ai.vision.face.models import FaceDetectionModel, FaceRecognitionModel, FaceAttributeTypeRecognition04, QualityForRecognition
import cv2
from openai import AzureOpenAI
from typing import Annotated, Literal
from pydantic import Field
from .utils._enums import OpensetFaceAttribConfig
import requests
import tempfile


def get_face_openset_attrib(
    file_path: Annotated[str, Field(description=OpensetFaceAttribConfig.ARGS_FILE_PATH)], 
    attribute_name: Annotated[str, Field(description=OpensetFaceAttribConfig.ARGS_ATTRIBUTE_NAME)],
    dilation: Annotated[float, Field(description=OpensetFaceAttribConfig.ARGS_DILATION)] = 1.25,
    is_url: Annotated[bool, Field(description=OpensetFaceAttribConfig.ARGS_IS_URL)] = False
):
    if file_path is None:
        return "The Azure AI Face API did not receive any image. Please provide an image."
    ENDPOINT = os.getenv("FACE_ENDPOINT")
    KEY = os.getenv("FACE_API_KEY")
    with FaceClient(
        endpoint=ENDPOINT, credential=AzureKeyCredential(KEY), 
        headers = {"X-MS-AZSDK-Telemetry": "sample=mcp-face-detect-openset-attr"}
    ) as face_client:
        if is_url is True:
            detected_faces = face_client.detect_from_url(
                url=file_path,
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=True,
            )
        else:
            if not os.path.exists(file_path):
                return f"Image file: {file_path} does not exist."
            
            detected_faces = face_client.detect(
                image_content=open(file_path, "rb"),
                detection_model=FaceDetectionModel.DETECTION03,
                recognition_model=FaceRecognitionModel.RECOGNITION04,
                return_face_id=True,
            )
    azure_client = AzureOpenAI(
        api_version="2025-03-01-preview",
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    )
    results = []
    dilation = 1.25
    if is_url:
        response = requests.get(file_path)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(response.content)
                file_path = tmp_file.name
        else:
            return f"Failed to download image from URL: {file_path} for openset face attribute detection."
    source_img = cv2.imread(file_path)
    for detected_face in detected_faces:
        cx = (detected_face.face_rectangle.left + 
              detected_face.face_rectangle.width / 2)
        cy = (detected_face.face_rectangle.top + 
              detected_face.face_rectangle.height / 2)
        w = detected_face.face_rectangle.width * dilation
        h = detected_face.face_rectangle.height * dilation
        dilated_rectangle = {
            "left": int(cx - w / 2),
            "top": int(cy - h / 2),
            "right": int(cx + w / 2),
            "bottom": int(cy + h / 2)
        }
        cropped_img = source_img[
            dilated_rectangle["top"]:dilated_rectangle["bottom"],
            dilated_rectangle["left"]:dilated_rectangle["right"]
        ]
        cropped_img = cv2.imencode(".jpg", cropped_img)[1]
        cropped_img_str = base64.b64encode(cropped_img).decode('utf-8')
        input_prompt = [
            { "type": "text", "text": f"What does the {attribute_name} "
                "attribute looks like in the following image? Response the "
                "answer in exactly one word." },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{cropped_img_str}",
                },
            }
        ]
        messages=[
            {
                "role": "user",
                "content": input_prompt
            }
        ]
        response = azure_client.chat.completions.create(
            model='gpt-4.1',
            messages=messages,
            max_tokens=20
        )
        response = response.choices[0].message.content
        result = f"""
        Open-set Face Detection Results: 
        'faceId': '{detected_face.face_id}', 
        '{attribute_name}': '{response}'
        """
        results.append(result)
    return "\n---\n".join(results)