from mcp.server.fastmcp import FastMCP
from tools.utils._enums import (
    CompareImagesConfig,
    CreateLPGConfig,
    EnrollFaceToLPGConfig,
    IdentifyFaceInLPGConfig,
    ListPersonsInLPGConfig,
    DeletePersonFromLPGConfig,
    DeleteFaceFromLPGConfig,
    OpensetFaceAttribConfig,
    AzureFaceAttribConfig,
    ListBlobFoldersConfig,
    ListPublicImageUrlsConfig,
    DownloadBlobFolderConfig,
)
from tools.CompareImages import compare_source_image_to_target_image
from tools.CreateLPG import create_large_person_group
from tools.EnrollFaceToLPG import enroll_face_to_group
from tools.IdentifyFaceInLPG import identify_face_from_group
from tools.ListPersonsInLPG import list_persons_in_group
from tools.DeleteFromLPG import delete_person_from_group, delete_face_from_group
from tools.OpensetFaceAttrib import get_face_openset_attrib
from tools.AzureFaceAttrib import get_face_dect
from tools.BlobFolderTools import (
    list_blob_folders_and_choose,
    list_public_image_urls,
    download_blob_folder_from_container,
)


class FaceMCPServer:
    def __init__(self):
        self.mcp = FastMCP("azure_ai_face_api")
        self.mcp.add_tool(
            name=CompareImagesConfig.TOOL_NAME,
            description=CompareImagesConfig.TOOL_DESC,
            fn=compare_source_image_to_target_image,
        )
        self.mcp.add_tool(
            name=CreateLPGConfig.TOOL_NAME,
            description=CreateLPGConfig.TOOL_DESC,
            fn=create_large_person_group,
        )
        self.mcp.add_tool(
            name=EnrollFaceToLPGConfig.TOOL_NAME,
            description=EnrollFaceToLPGConfig.TOOL_DESC,
            fn=enroll_face_to_group,
        )
        self.mcp.add_tool(
            name=IdentifyFaceInLPGConfig.TOOL_NAME,
            description=IdentifyFaceInLPGConfig.TOOL_DESC,
            fn=identify_face_from_group,
        )
        self.mcp.add_tool(
            name=ListPersonsInLPGConfig.TOOL_NAME,
            description=ListPersonsInLPGConfig.TOOL_DESC,
            fn=list_persons_in_group,
        )
        self.mcp.add_tool(
            name=DeletePersonFromLPGConfig.TOOL_NAME,
            description=DeletePersonFromLPGConfig.TOOL_DESC,
            fn=delete_person_from_group,
        )
        self.mcp.add_tool(
            name=DeleteFaceFromLPGConfig.TOOL_NAME,
            description=DeleteFaceFromLPGConfig.TOOL_DESC,
            fn=delete_face_from_group,
        )
        self.mcp.add_tool(
            name=OpensetFaceAttribConfig.TOOL_NAME,
            description=OpensetFaceAttribConfig.TOOL_DESC,
            fn=get_face_openset_attrib,
        )
        self.mcp.add_tool(
            name=AzureFaceAttribConfig.TOOL_NAME,
            description=AzureFaceAttribConfig.TOOL_DESC,
            fn=get_face_dect,
        )
        self.mcp.add_tool(
            name=ListBlobFoldersConfig.TOOL_NAME,
            description=ListBlobFoldersConfig.TOOL_DESC,
            fn=list_blob_folders_and_choose,
        )
        self.mcp.add_tool(
            name=ListPublicImageUrlsConfig.TOOL_NAME,
            description=ListPublicImageUrlsConfig.TOOL_DESC,
            fn=list_public_image_urls,
        )
        self.mcp.add_tool(
            name=DownloadBlobFolderConfig.TOOL_NAME,
            description=DownloadBlobFolderConfig.TOOL_DESC,
            fn=download_blob_folder_from_container,
        )

    def run(self):
        self.mcp.run(transport="stdio")


def run_server():
    server = FaceMCPServer()
    server.run()
