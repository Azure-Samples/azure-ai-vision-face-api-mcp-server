import os
from typing import Annotated
from pydantic import Field
from azure.ai.vision.face import FaceAdministrationClient, FaceClient
from azure.core.credentials import AzureKeyCredential

from .utils._enums import ListPersonsInLPGConfig


def list_persons_in_group(
    group_uuid: Annotated[
        str, Field(description=ListPersonsInLPGConfig.ARGS_GROUP_UUID)
    ],
):
    ENDPOINT = os.getenv("AZURE_FACE_ENDPOINT")
    KEY = os.getenv("AZURE_FACE_API_KEY")
    output_list = []
    with FaceAdministrationClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(KEY),
        headers={"X-MS-AZSDK-Telemetry": "sample=mcp-face-reco-list-persons"},
    ) as face_admin_client:
        persons = face_admin_client.large_person_group.get_persons(
            large_person_group_id=group_uuid
        )
        if not persons:
            return f"No persons found in the group with UUID: {group_uuid}"
        for person in persons:
            num_faces = len(person.persisted_face_ids or [])
            output_list.append(
                f"Person ID: {person.person_id}, "
                f"Name: {person.name}, "
                f"Number of faces: {num_faces}"
            )
    return "\n".join(output_list)
