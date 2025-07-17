
import os
import uuid

from azure.ai.vision.face import FaceAdministrationClient
from azure.ai.vision.face.models import FaceRecognitionModel
from azure.core.credentials import AzureKeyCredential


def create_large_person_group():
    ENDPOINT = os.getenv("FACE_ENDPOINT")
    KEY = os.getenv("FACE_API_KEY")
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