from mcp.server.fastmcp import FastMCP

import os
import base64

from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceAdministrationClient
from azure.ai.vision.face.models import FaceDetectionModel, FaceRecognitionModel
import cv2
from openai import AzureOpenAI
from typing import Annotated, Literal
from pydantic import Field
from .utils._enums import CreateLPGConfig


def create_large_person_group():
    ENDPOINT = os.getenv("FACE_ENDPOINT")
    KEY = os.getenv("FACE_API_KEY")
    import uuid
    group_uuid = str(uuid.uuid4())

    with FaceAdministrationClient(
        endpoint=ENDPOINT, credential=AzureKeyCredential(KEY), 
        headers = {"X-MS-AZSDK-Telemetry": "sample=mcp-face-reco-create-lpg"}
    ) as face_admin_client:
        face_admin_client.large_person_group.create(
            large_person_group_id=group_uuid,
            name=group_uuid,
            recognition_model=FaceRecognitionModel.RECOGNITION04,
        )
    return f"Create a large person group with UUID: {group_uuid} successfully."