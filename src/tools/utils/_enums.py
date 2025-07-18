from enum import Enum

class CompareImagesConfig(str, Enum):
    TOOL_NAME = "azure_face_recognition_compare_two_images"
    TOOL_DESC = "Compare the similarity of faces in two images to determine if they belong to the same person. This function supports three comparison modes: 'largest_face', 'most_similar', and 'exhaustive'. YOU (MCP) must ask the user to choose one of these modes for each comparison with detailed explanation for each mode. YOU (MCP) must use the exact same explanation as following: 'largest_face' will compare only the largest face in both image, 'most_similar' will find the most similar face in the target image from each face in source image, and 'exhaustive' will compare all faces in both images."
    ARGS_SOURCE_IMAGE = "The absolute file path to the source image file. If the file path is the local file path, complete and fix the file path. If the source image is the remote file path URL, set is_source_image_url to True."
    ARGS_TARGET_IMAGE = "The absolute file path to the target image file. If the file path is the local file path, complete and fix the file path. If the target image is the remote file path URL, set is_target_image_url to True."
    ARGS_IS_SOURCE_IMAGE_URL = "Whether the source image is a remote file URL or a local file path. YOU (MCP) should set this to True if the source image is a URL, otherwise set it to False."
    ARGS_IS_TARGET_IMAGE_URL = "Whether the target image is a remote file URL or a local file path. YOU (MCP) should set this to True if the target image is a URL, otherwise set it to False."
    ARGS_COMPARISON_MODE = "The mode of comparison: 'largest_face', 'most_similar', or 'exhaustive'. When source_image or target_image contains more than one face, 'exhaustive' will compare all faces in both images, 'most_similar' will use the find_similar API to determine the best match for each face in the source image, and 'largest_face' will compare only the largest face in each image. YOU (MCP) must ask the user to choose one of these modes for each comparison with detail explanation for each mode."
    ARGS_THRESHOLD = "The threshold for determining if two faces are identical. Default is 0.5."


class CreateLPGConfig(str, Enum):
    TOOL_NAME = "azure_face_recognition_create_large_person_group"
    TOOL_DESC = "Create a large person group for face recognition leveraging the azure ai face recognition API."


class EnrollFaceToLPGConfig(str, Enum):
    TOOL_NAME = "azure_face_recognition_enroll"
    TOOL_DESC = "Enroll a new person to a specific large person group leveraging the azure ai face recognition API."
    ARGS_FILE_PATH_LIST = "A list of absolute file paths to the image files. If the file_path is the local file path, complete and fix the file_path. If the file_path is the remote file_path URL, set is_url to True."
    ARGS_IS_URL = "Whether the file_path is a remote file URL or a local file path. YOU (MCP) should set this to True if the file_path is a URL, otherwise set it to False."
    ARGS_PERSON_NAME = "The human-readable name of the person to be enrolled."
    ARGS_GROUP_UUID = "The UUID of the person group to which the person will be enrolled."
    ARGS_CHECK_QUALITY = "Whether to check the quality of the images before enrolling. Default is True. If set to True, the function will check if the images are suitable for face recognition and will not enroll if the quality is insufficient."


class IdentifyFaceInLPGConfig(str, Enum):
    TOOL_NAME = "azure_face_recognition_identify"
    TOOL_DESC = "Identify a face from a specific large person group leveraging the azure ai face recognition API."
    ARGS_FILE_PATH = "The absolute file path to the image file. If the file_path is the local file path, complete and fix the file_path. If the file_path is the remote file_path URL, set is_url to True."
    ARGS_GROUP_UUID = "The UUID of the person group in which to identify the face."
    ARGS_IS_URL = "Whether the file_path is a remote file URL or a local file path. YOU (MCP) should set this to True if the file_path is a URL, otherwise set it to False."


class OpensetFaceAttribConfig(str, Enum):
    TOOL_NAME = "azure_face_detection_openset_attribute"
    TOOL_DESC = "Get the face attribute from the user provided images. This function supports all the possible face or image attributes but excludes the attributes closely related to the following: head pose, glasses, occlusion, blur, exposure, mask, quality, age, and landmarks. This function could be used separately or after the 'azure_face_detection_attribute' function if the user potentially needs any other attribute which is not supported by the 'azure_face_detection_attribute' function. YOU (MCP) must return the error message if the Azure OpenAI configuration file is not set correctly or the image file is not provided."
    ARGS_FILE_PATH = "The absolute file path to the image file. If the file_path is the local file path, complete and fix the file_path. If the file_path is the remote file_path URL, set is_url to True."
    ARGS_ATTRIBUTE_NAME = "The name of the attribute to retrieve."
    ARGS_DILATION = "The dilation factor to apply to the detected face rectangle. Default is 1.25, which enlarges the rectangle by 25% on each dimension."
    ARGS_IS_URL = "Whether the file_path is a remote file URL or a local file path. YOU (MCP) should set this to True if the file_path is a URL, otherwise set it to False."
    ERROR_AOAI_NOT_CONFIGURED = "The Azure OpenAI did not receive any image. To enable open-set face attribute detection, you need access to Azure OpenAI. Please check your .vscode/mcp.json configuration file and ensure the AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are set correctly. After setting the environment variables, please restart the MCP server and try again."

class AzureFaceAttribConfig(str, Enum):
    TOOL_NAME = "azure_face_detection_attribute"
    TOOL_DESC = "Detect and analyze the user provided images' attribute. Get all the face detection results from the face detection API. This function only supports the following face attribute: head pose, glasses, occlusion, blur, exposure, mask, quality, age, and landmarks. If the user potentially needs any other attribute which is not supported by this function, YOU (MCP) should call the 'azure_face_detection_openset_attribute' function after finishing this function."
    ARGS_FILE_PATH = "The absolute file path to the image file. If the file_path is the local file path, complete and fix the file_path. If the file_path is the remote file_path URL, set is_url to True."
    ARGS_IS_URL = "Whether the file_path is a remote file URL or a local file path. YOU (MCP) should set this to True if the file_path is a URL, otherwise set it to False."
    ARGS_RETURN_HEAD_POSE = "Whether to return head pose information. Default is False. The information is 3-D roll/yaw/pitch angles for face direction."
    ARGS_RETURN_GLASSES = "Whether to return glasses information. Default is False. The information is Glasses type. Values include 'NoGlasses', 'ReadingGlasses', 'Sunglasses', 'SwimmingGoggles'."
    ARGS_RETURN_OCCLUSION = "Whether to return occlusion information. Default is False. The information is Whether each facial area is occluded, including forehead, eyes and mouth."
    ARGS_RETURN_BLUR = "Whether to return blur information. Default is False. The information is Face is blurry or not. Level returns 'Low', 'Medium' or 'High'. Value returns a number between [0,1], the larger the blurrier."
    ARGS_RETURN_EXPOSURE = "Whether to return exposure information. Default is False. The information is Face exposure level. Level returns 'GoodExposure', 'OverExposure' or 'UnderExposure'."
    ARGS_RETURN_MASK = "Whether to return mask information. Default is False. The information is Whether each face is wearing a mask. Mask type returns 'noMask', 'faceMask', 'otherMaskOrOcclusion', or 'uncertain'. Value returns a boolean 'noseAndMouthCovered' indicating whether nose and mouth are covered."
    ARGS_RETURN_QUALITY_FOR_RECOGNITION = "Whether to return quality for recognition information. Default is False. The information is The overall image quality regarding whether the image being used in the detection is of sufficient quality to attempt face recognition on. The value is an informal rating of low, medium, or high. Only 'high' quality images are recommended for person enrollment and quality at or above 'medium' is recommended for identification scenarios."
    ARGS_RETURN_AGE = "Whether to return age information. Default is False. The information is Age in years."
    ARGS_RETURN_LANDMARKS = "Whether to return Facial landmarks information. Default is False."