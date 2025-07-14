# Azure AI Vision Face API MCP Server
Introducing a Face Detection and Recognition MCP Server to allow the embedding of face attribute detection and similar face recognition during Agentic AI workflows.


## Face Detection and Recognition API
For more information, visit [Face API](https://learn.microsoft.com/en-us/rest/api/face/operation-groups?view=rest-face-v1.2)

## Running MCP Server
### add dependency
1. Using PIP
```bash
pip install --upgrade azure-ai-vision-face opencv-python openai fastmcp
```

2. Sample for vs code

Rename `.vscode/mcp-bp.json` to `.vscode/mcp.json` and fill up the full python path and the api key. The required environment variables are `FACE_ENDPOINT` and `FACE_API_KEY`.
```json
{
  "servers": {
    "face_dec":{
      "command": "/path/to/python",
      "args": ["/path/to/Face-MCP/server.py"],
      "env": {
        "AZURE_OPENAI_ENDPOINT":"aoai_endpoint",
        "AZURE_OPENAI_API_KEY":"aoai_key",
        "FACE_ENDPOINT":"faceapi_endpoint",
        "FACE_API_KEY":"faceapi_key"
      }
    }
  }
}
```

3. (Optional) Create a GPT deployment on Azure OpenAI:
To enable the open-set face attribute detection, you should setup a deployment of gpt-4.1 on Azure OpenAI and fill up the environment variables `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`. For more information, visit [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/overview)

4. Open this folder using VScode and start to chat with GitHub Copilot (using Agent mode with gpt-4.1)!

## Example Prompts
### Face Attribute Detection
1. Test the face attribute detection:
```
Check all the faces inside detection1.jpg wearing the mask or glasses
```

2. Test the open-set attribute detection:
```
Analyze the hair color and gender of all individuals in detection2.jpg
```

3. Test the attribute detection using image URL:
```
Check all the faces' age and gender inside https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/refs/heads/master/Face/images/detection4.jpg
```

### Face Recognition
1. Test the face enrollment and identify without handling any uuid by user:
```
create a new person group and enroll all the images in the example/reco folder and check example/test-image-person-group.jpg belongs to which person with which person id. Also check the follow image belongs to which person: https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/refs/heads/master/Face/images/extra-woman-image.jpg
```

### Image Comparison
1. Compare the similarity between two images:
```
Compare the identification1.jpg with https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/refs/heads/master/Face/images/findsimilar.jpg
```

2. Compare two folders:
```
Compare all the images in reco/Bob and with reco/Emily
```