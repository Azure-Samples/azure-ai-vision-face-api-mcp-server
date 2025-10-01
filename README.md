# Azure AI Vision Face API MCP Server
Introducing a Face Detection and Recognition MCP Server to allow the embedding of face attribute detection and face recognition during Agentic AI workflows.


https://raw.githubusercontent.com/Azure-Samples/azure-ai-vision-face-api-mcp-server/refs/heads/main/assets/MCP_Intro.mp4

## Face Detection and Recognition API
For more information, visit [Face API](https://learn.microsoft.com/en-us/rest/api/face/operation-groups?view=rest-face-v1.2)

## Running MCP Server
### Installation
#### 1. Using UV
Refer to the [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2) for instructions on installing uv.

#### 2. Clone this project
We provide several example images in the [example](example) folder. Please clone this project to try the [example prompts](#example-prompts) below.
```bash
git clone https://github.com/Azure-Samples/azure-ai-vision-face-api-mcp-server.git
```

#### 3. Set Up Azure AI Vision Face API
- Go to the [Azure Portal](https://portal.azure.com/#create/Microsoft.CognitiveServicesFace) and create a new **Face** resource.
- After deployment, navigate to the resource and copy the **Endpoint URL** and one of the **Key** from the "Keys and Endpoint" section.
- You will be prompted to enter the following environment variables the first time you start the MCP server:
  - `Azure AI Face API Endpoint`: The endpoint URL of your Azure Face API deployment.
  - `Azure AI Face API Key`: The API key for your Azure Face API resource.

#### 4. (Optional) Deploy GPT-4.1 on Azure OpenAI for Open-Set Attribute Detection
- To enable open-set face attribute detection, you need access to Azure OpenAI.
- In the [Azure Portal](https://portal.azure.com/), create an Azure OpenAI resource and deploy a GPT-4.1 model.
- Once deployed, obtain the **Endpoint URL** and **API Key** for your OpenAI resource.
- You will be prompted to enter the following environment variables the first time you start the MCP server:
  - `Azure OpenAI Endpoint`: The endpoint URL of your Azure OpenAI deployment.
  - `Azure OpenAI API Key`: The API key for your Azure OpenAI resource.
- For more details about using , see the [Azure OpenAI documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/overview).

#### 5. (Optional) Configure Azure Storage for Image Management
- To enable image management and access, you need an Azure Storage account.
- In the [Azure Portal](https://portal.azure.com/), create an Azure Storage resource and set up a container for your images.
- Once created, obtain your **Storage Account Name**, **Container Name**, and a **SAS Token** for secure access.
- You will be prompted to enter the following environment variables the first time you start the MCP server:
  - `AZURE STORAGE ACCOUNT`: The name of your Azure Storage account.
  - `AZURE STORAGE CONTAINER`: The name of your image container.
  - `AZURE STORAGE SAS TOKEN`: The SAS token for your storage container.
- For more details about using Azure Storage, see the [Azure Storage documentation](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview).

#### 6. Interact with our MCP tools using Visual Studio Code GitHub Copilot
- Install [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) Visual Studio Code extension.
- Rename the file `.vscode/mcp-bp.json` to `.vscode/mcp.json` (or copy `.vscode/mcp-bp.json` to your existing `.vscode/mcp.json`) and press `Start` above the `azure_ai_vision_face_api_mcp_server` in `.vscode/mcp.json`.
- Follow this [guide](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server) to add our MCP tools in the workspace and [start a conversation with GitHub Copilot](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode) and use MCP tools in agent mode leveraging GPT-4.1.

#### 7. (Optional) Prepare Environment for Local Testing
- Before running pytest or other scripts outside of MCP, copy `.env.example` to `.env`.
- Fill in your real keys in `.env`. These keys are the same as those used in `.vscode/mcp.json`.

#### 8. (Optional) MCP HTTP Bridge (Node/TypeScript)

- This repo includes a small **HTTP bridge** in the `bridge/` folder.
- The bridge launches the local **Azure Face MCP server** (via `uvx --from …`) using stdio and exposes a REST API for listing and calling MCP tools.
- It makes the MCP server usable from **OpenAI Responses API** or any web frontend.
- **Available endpoints**
  - GET /health → { ok: true }
  - GET /mcp/tools → list available MCP tools
  - POST /mcp/call → call a tool by name with arguments
**Usage**
  ```bash
  # Setup
  cd bridge
  npm install
  cp .env.example .env   # fill in your environment values (see step 7 above)
  npm run dev

  # Examples:
  # list all MCP tools
  curl http://127.0.0.1:8787/mcp/tools
  # list all large person groups
  curl --% -X POST http://127.0.0.1:8787/mcp/call -H "Content-Type: application/json" -d "{ \"name\": \"azure_face_recognition_list_large_person_groups\", \"arguments\": {} }"
  ```

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