import express from "express";
import cors from "cors";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { z } from "zod";

const app = express();

app.use(cors());

app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl}`);
  next();
});

function createServer() {
  const server = new McpServer({
    name: "gtm-helix-competitive-intelligence-copilot",
    version: "1.0.0"
  });

  server.tool(
    "health_check",
    "Simple health check tool",
    {},
    async () => {
      return {
        content: [
          {
            type: "text",
            text: "MCP server is running."
          }
        ]
      };
    }
  );

  server.tool(
    "competitive_scenario",
    "Run a competitive intelligence scenario",
    {
      company: z.string().describe("Company name"),
      competitor: z.string().describe("Competitor name"),
      scenario: z.string().describe("Scenario to analyze")
    },
    async ({ company, competitor, scenario }) => {
      return {
        content: [
          {
            type: "text",
            text:
              `Competitive scenario analysis\n\n` +
              `Company: ${company}\n` +
              `Competitor: ${competitor}\n` +
              `Scenario: ${scenario}\n\n` +
              `Status: Placeholder response from Railway MCP server.\n` +
              `Confidence: Medium\n` +
              `Recommended action: Review scenario manually and expand tool logic.`
          }
        ]
      };
    }
  );

  return server;
}

const sessions = new Map();

app.get("/", (req, res) => {
  res.status(200).send("OK");
});

app.get("/health", (req, res) => {
  res.status(200).json({ ok: true });
});

app.get("/sse", async (req, res) => {
  try {
    const server = createServer();
    const transport = new SSEServerTransport("/messages", res);
    const sessionId = transport.sessionId;

    sessions.set(sessionId, { server, transport });
    console.log(`SSE session opened: ${sessionId}`);

    res.on("close", async () => {
      console.log(`SSE session closed: ${sessionId}`);
      const entry = sessions.get(sessionId);
      sessions.delete(sessionId);

      if (entry) {
        try {
          await entry.transport.close();
        } catch (error) {
          console.error("Transport close error:", error);
        }
      }
    });

    await server.connect(transport);
  } catch (error) {
    console.error("SSE connection error:", error);
    if (!res.headersSent) {
      res.status(500).send("Internal Server Error");
    }
  }
});

app.post("/messages", async (req, res) => {
  const sessionId = req.query.sessionId;

  console.log(`POST /messages sessionId=${sessionId}`);

  try {
    if (!sessionId || !sessions.has(sessionId)) {
      return res.status(400).json({ error: "Invalid or missing sessionId" });
    }

    const { transport } = sessions.get(sessionId);

    console.log(`Handling MCP message for session ${sessionId}`);
    await transport.handlePostMessage(req, res);
    console.log(`Handled MCP message for session ${sessionId}`);
  } catch (error) {
    console.error("Message handling error:", error);
    if (!res.headersSent) {
      res.status(500).json({ error: "Internal Server Error" });
    }
  }
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`MCP server listening on http://localhost:${port}/sse`);
});