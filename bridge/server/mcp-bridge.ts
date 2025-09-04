import express from "express";
import path from "node:path";
import dotenv from "dotenv";
import { fileURLToPath } from "node:url";
import { Client } from "@modelcontextprotocol/sdk/client";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio";

// Resolve paths and load environment variables
const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, "..", "..");
dotenv.config({ path: path.join(repoRoot, ".env") });

// Environment/configuration
const MCP_COMMAND = process.env.MCP_COMMAND ?? "uvx";
const MCP_ARGS = (process.env.MCP_ARGS ?? "--from git+https://github.com/Azure-Samples/azure-ai-vision-face-api-mcp-server azure-face-mcp")
    .split(" ")
    .filter(Boolean);
const MCP_CWD = process.env.MCP_CWD ?? repoRoot;
const PORT = Number(process.env.MCP_BRIDGE_PORT ?? 8787);

// MCP client factory
async function makeMcpClient() {
    const transport = new StdioClientTransport({
        command: MCP_COMMAND,
        args: MCP_ARGS,
        cwd: MCP_CWD,
        env: process.env,
    });
    const client = new Client({ name: "face-web-bridge", version: "0.1.0" });
    await client.connect(transport);
    return { client, transport };
}

// Utility to run with MCP client
async function withClient<T>(fn: (client: Client) => Promise<T>) {
    const { client, transport } = await makeMcpClient();
    try {
        return await fn(client);
    } finally {
        await transport.close();
    }
}

// Express app setup
const app = express();
app.use(express.json({ limit: "10mb" }));

app.get("/health", (_req, res) => res.json({ ok: true }));

app.get("/mcp/tools", async (_req, res) => {
    try {
        const tools = await withClient(c => c.listTools());
        res.json(tools);
    } catch (e: any) {
        res.status(500).json({ error: e.message });
    }
});

app.post("/mcp/call", async (req, res) => {
    const { name, arguments: args } = req.body ?? {};
    if (!name) return res.status(400).json({ error: "name required" });
    try {
        const result = await withClient(c => c.callTool({ name, arguments: args ?? {} }));
        res.json(result);
    } catch (e: any) {
        res.status(500).json({ error: e.message });
    }
});

app.listen(PORT, () => {
    console.log(`[MCP bridge] listening on http://127.0.0.1:${PORT} (cwd=${MCP_CWD})`);
});
