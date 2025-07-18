# Azure AI Vision Face API MCP Server
Introducing a Face Detection and Recognition MCP Server to allow the embedding of face attribute detection and similar face recognition during Agentic AI workflows.


## Face Detection and Recognition API
For more information, visit [Face API](https://learn.microsoft.com/en-us/rest/api/face/operation-groups?view=rest-face-v1.2)

## Running MCP Server
### Installation
#### 1. Using PIP with python 3.10+
```bash
git clone https://github.com/Azure-Samples/azure-ai-vision-face-api-mcp-server.git
cd azure-ai-vision-face-api-mcp-server
pip install -r requirements.txt
```

#### 2. Set Up Azure AI Vision Face API
- Go to the [Azure Portal](https://portal.azure.com/#create/Microsoft.CognitiveServicesFace) and create a new **Face** resource.
- After deployment, navigate to the resource and copy the **Endpoint URL** and one of the **Key** from the "Keys and Endpoint" section.
- You will set the following environment variables in your [configuration](.vscode/mcp-bp.json):
  - `FACE_ENDPOINT`: The endpoint URL of your Azure Face API deployment.
  - `FACE_API_KEY` : The API key for your Azure Face API resource.

#### 3. (Optional) Deploy GPT-4.1 on Azure OpenAI for Open-Set Attribute Detection
- To enable open-set face attribute detection, you need access to Azure OpenAI.
- In the [Azure Portal](https://portal.azure.com/), create an Azure OpenAI resource and deploy a GPT-4.1 model.
- Once deployed, obtain the **Endpoint URL** and **API Key** for your OpenAI resource.
- You will set the following environment variables in your [configuration](.vscode/mcp-bp.json):
  - `AZURE_OPENAI_ENDPOINT`: The endpoint URL of your Azure OpenAI deployment.
  - `AZURE_OPENAI_API_KEY`: The API key for your Azure OpenAI resource.
- For more details about using , see the [Azure OpenAI documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/overview).

#### 4. Configure VS Code for MCP Server Integration
- Copy the file `.vscode/mcp-bp.json` and rename it to `.vscode/mcp.json` in your project directory.
- Edit `.vscode/mcp.json` and fill up the full python path and the api key. The required environment variables are `FACE_ENDPOINT` and `FACE_API_KEY` .
- Example configuration:
  ```json
  {
    "servers": {
      "azure_ai_vision_face_api_mcp_server": {
        "command": "/path/to/python",
        "args": ["/path/to/azure-ai-vision-face-api-mcp-server/server.py"],
        "env": {
          "FACE_ENDPOINT": "your_faceapi_endpoint",
          "FACE_API_KEY": "your_faceapi_key",
          "AZURE_OPENAI_ENDPOINT": "your_aoai_endpoint",
          "AZURE_OPENAI_API_KEY": "your_aoai_key"
        }
      }
    }
  }
  ```

#### 5. Interact with our MCP tools using Visual Studio Code GitHub Copilot
- Install [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) Visual Studio Code extension.
- Follow this [guide](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server) to add our MCP tools in the workspace and [start a conversation with GitHub Copilot](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode) and use MCP tools in agent mode leveraging GPT-4.1.

## Example Prompts
- You may be prompted to agree to use the MCP tool the first time you use each MCP tool. Please press `Continue` to proceed.
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

2. Compare the similarity between one image and another image folder:
```
Compare test-image-person-group.jpg with all the images in reco/Bob" using the "most_similar" option
```

### Face Recognition
1. Test the face enrollment and identify without handling any uuid by user:
```
create a new person group and enroll all the images in the example/reco folder and check example/test-image-person-group.jpg belongs to which person with which person id. Also check the following image belongs to which person: https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/refs/heads/master/Face/images/extra-woman-image.jpg
```