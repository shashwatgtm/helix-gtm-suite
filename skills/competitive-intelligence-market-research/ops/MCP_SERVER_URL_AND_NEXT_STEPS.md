# MCP Server URL and Next Steps (Railway-First, 24x7)

You are correct: a local MCP server is only for temporary testing. If your laptop sleeps/shuts down, local MCP stops. Use Railway so the URL stays live 24x7.

## 0) Quick RCA: why the setup felt confusing (recursive)
1. **Symptom:** "I don't understand what to copy."
2. **Why #1:** Instructions were grouped into one large block.
3. **Why #2:** Large blocks hide where one command ends and the next starts.
4. **Why #3:** Mixed context (PowerShell + Railway dashboard + ChatGPT connector) made execution order unclear.
5. **Why #4:** Fail state (`Deploy failed`) was not paired with an immediate "do this exact diagnostic command" path.
6. **Why #5 (root cause):** Guidance was technically correct, but not operationally chunked for first-time users.

**Fix applied in this doc:** one command at a time, explicit location (Windows PowerShell), and a strict failure branch.

---

## 1) Where to run commands
Run every command below in **Windows PowerShell** on your laptop (not inside Railway website terminal).

---

## 2) Copy-paste commands one by one

### Step A — Create project folder
```powershell
Set-Location C:\Users\shash
New-Item -ItemType Directory -Path .\mcp-ci-server -Force | Out-Null
Set-Location .\mcp-ci-server
```

### Step B — Initialize Node project
```powershell
npm init -y
npm install @modelcontextprotocol/sdk express cors zod
```

### Step C — Create `server.js`
```powershell
@'
import express from "express";
import cors from "cors";
import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

const app = express();
app.use(cors());
app.use(express.json());

const server = new McpServer({ name: "gtm-helix-mcp", version: "0.1.0" });

server.tool(
  "health_check",
  { message: z.string().optional() },
  async ({ message }) => ({
    content: [{ type: "text", text: "MCP OK: " + (message ?? "ready") }]
  })
);

const transports = new Map();

app.get("/sse", async (_req, res) => {
  const transport = new SSEServerTransport("/messages", res);
  transports.set(transport.sessionId, transport);
  res.on("close", () => transports.delete(transport.sessionId));
  await server.connect(transport);
});

app.post("/messages", async (req, res) => {
  const sessionId = req.query.sessionId;
  const transport = transports.get(sessionId);
  if (!transport) {
    res.status(400).json({ error: "Invalid or missing sessionId" });
    return;
  }
  await transport.handlePostMessage(req, res);
});

const port = process.env.PORT || 8787;
app.listen(port, () => {
  console.log("MCP server listening on http://localhost:" + port + "/sse");
});
'@ | Set-Content -Path .\server.js -Encoding UTF8
```

### Step D — Ensure `package.json` start script is correct
```powershell
$pkg = Get-Content .\package.json -Raw | ConvertFrom-Json
$pkg.type = "module"
$pkg.main = "server.js"
if ($null -eq $pkg.scripts) { $pkg | Add-Member -NotePropertyName scripts -NotePropertyValue (@{}) -Force }
$pkg.scripts.start = "node server.js"
$pkg | ConvertTo-Json -Depth 20 | Set-Content .\package.json -Encoding UTF8
```

### Step E — Deploy to Railway
```powershell
railway login
railway init
railway up
railway domain
```

---

## 3) If `railway up` fails, do this immediately
Copy-paste these diagnostics and share outputs:

```powershell
railway status
railway logs
railway domain
curl.exe -i https://competitive-intelligence-production-29d2.up.railway.app/sse
```

If curl shows Railway "Not Found / train has not arrived", deployment is not healthy yet. Fix deploy first, then test connector.

---

## 4) Final MCP URL format for ChatGPT connector
Use:
- `https://<your-railway-app>.up.railway.app/sse`

For your current project, likely:
- `https://competitive-intelligence-production-29d2.up.railway.app/sse`

---

## 5) Next steps after MCP is healthy
1. Continue `ops/CHATGPT_STORE_SUBMISSION_PLAYBOOK.md`
2. Run smoke tests
3. Submit for review
