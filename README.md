# Azure AI Vision Face API MCP Server
Introducing a Face Detection and Recognition MCP Server to allow the embedding of face attribute detection and similar face recognition during Agentic AI workflows.


## Face Detection and Recognition API
For more information, visit [Face API](https://learn.microsoft.com/en-us/rest/api/face/operation-groups?view=rest-face-v1.2)

## Running MCP Server
### Installation
#### 1. Using PIP with python 3.10+
```bash
pip install -r requirements.txt
```

#### 2. Azure AI Vision Face API
[Create a Face resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesFace) in the Azure portal and obtain a key and endpoint URL to call face API.

#### 3. Sample for VS Code
Rename `.vscode/mcp-bp.json` to `.vscode/mcp.json` and fill up the full python path and the api key. The required environment variables are `FACE_ENDPOINT` and `FACE_API_KEY`.
```json
{
  "servers": {
    "face_dec":{
      "command": "/path/to/python",
      "args": ["/path/to/Face-MCP/server.py"],
      "env": {
        "FACE_ENDPOINT":"faceapi_endpoint",
        "FACE_API_KEY":"faceapi_key",
        "AZURE_OPENAI_ENDPOINT":"aoai_endpoint",
        "AZURE_OPENAI_API_KEY":"aoai_key"
      }
    }
  }
}
```

#### 4. (Optional) Create a GPT deployment on Azure OpenAI
To enable the open-set face attribute detection, you should setup a deployment of gpt-4.1 on Azure OpenAI and fill up the environment variables `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`. For more information, visit [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/overview)

#### 5. Interact with our MCP tools using VS Code Copilot
Follow this [guide](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server) to add our MCP tools in the workspace and [start a conversation with GitHub Copilot](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode) and use MCP tools in agent mode leveraging GPT-4.1.

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

### Face Image Comparison
1. Compare the similarity between two face images:
```
Compare the identification1.jpg with https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/refs/heads/master/Face/images/findsimilar.jpg
```

2. Compare two folders containing multiple face images:
```
Compare all the images in reco/Bob and with reco/Emily
```

### Face Recognition
1. Test the face enrollment and identify without handling any uuid by user:
```
create a new person group and enroll all the images in the example/reco folder and check example/test-image-person-group.jpg belongs to which person with which person id. Also check the following image belongs to which person: https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/refs/heads/master/Face/images/extra-woman-image.jpg
```