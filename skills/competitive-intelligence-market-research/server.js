import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import express from "express";
import cors from "cors";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { z } from "zod";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());

app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl}`);
  next();
});

function readText(relativePath) {
  try {
    return fs.readFileSync(path.join(__dirname, relativePath), "utf8");
  } catch {
    return "";
  }
}

function extractSection(markdown, heading) {
  if (!markdown) return "";
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(`##\\s+${escaped}\\s*([\\s\\S]*?)(?=\\n##\\s+|$)`, "i");
  const match = markdown.match(regex);
  return match ? match[1].trim() : "";
}

function cleanInline(text) {
  return String(text || "")
    .replace(/`/g, "")
    .replace(/\*\*/g, "")
    .replace(/\r/g, "")
    .trim();
}

function cleanBulletLines(sectionText) {
  return cleanInline(sectionText)
    .split("\n")
    .map((line) => line.replace(/^\s*[-*]\s*/, "").trim())
    .filter(Boolean);
}

function parseScenarioCard(fileName) {
  const fullPath = path.join(__dirname, "scenarios", fileName);
  const markdown = fs.readFileSync(fullPath, "utf8");
  const headingMatch = markdown.match(/^#\s*([A-Z]{2}-\d{2})\s*[—-]\s*(.+)$/m);
  const id = headingMatch ? headingMatch[1].trim().toUpperCase() : fileName.replace(".md", "").toUpperCase();
  const title = headingMatch ? headingMatch[2].trim() : fileName.replace(".md", "");
  const primaryJtbdMatch = markdown.match(/##\s+Primary JTBD\s*`([^`]+)`/i);
  const primaryJtbd = primaryJtbdMatch ? primaryJtbdMatch[1].trim().toLowerCase() : "";
  const typicalBuyer = cleanInline(extractSection(markdown, "Typical Buyer / Operator")).replace(/^Primary economic buyer in this vertical:\s*/i, "");
  const analysisLens = cleanBulletLines(extractSection(markdown, "Analysis Lens"));
  const freeLayerDeliverable = cleanBulletLines(extractSection(markdown, "Free-Layer Deliverable"));
  const outputEmphasis = cleanBulletLines(extractSection(markdown, "Output Emphasis"));
  const scenarioArtifact = cleanInline(extractSection(markdown, "Scenario Artifact"));
  const constraints = cleanBulletLines(extractSection(markdown, "Constraints"));
  const preferredHandoffBoundary = cleanBulletLines(extractSection(markdown, "Preferred Handoff Boundary"));

  return {
    id,
    title,
    primaryJtbd,
    typicalBuyer,
    analysisLens,
    freeLayerDeliverable,
    outputEmphasis,
    scenarioArtifact,
    constraints,
    preferredHandoffBoundary
  };
}

function loadScenarioCards() {
  const dir = path.join(__dirname, "scenarios");
  if (!fs.existsSync(dir)) return {};
  const entries = fs.readdirSync(dir).filter((name) => name.toLowerCase().endsWith(".md"));
  const cards = {};
  for (const fileName of entries) {
    const card = parseScenarioCard(fileName);
    cards[card.id] = card;
  }
  return cards;
}

const DOCS = {
  inputContract: readText("chatgpt/INPUT_CONTRACT.md"),
  outputSchema: readText("chatgpt/OUTPUT_SCHEMA.md"),
  systemPrompt: readText("chatgpt/SYSTEM_PROMPT.md"),
  taxonomy: readText("chatgpt/TAXONOMY_STANDARD.md"),
  scenarioIndex: readText("chatgpt/SCENARIO_INDEX.md"),
  userFlow: readText("chatgpt/USER_FLOW.md"),
  statusTemplates: readText("chatgpt/STATUS_NOTIFICATION_TEMPLATES.md"),
  paywall: readText("growth/PAYWALL_AND_CTA.md")
};

const SCENARIO_CARDS = loadScenarioCards();

const ROLE_VALUES = ["founder", "pmm", "sales-leader", "strategy", "inferred-other"];
const JTBD_VALUES = [
  "market-sizing",
  "feature-gap-analysis",
  "pricing-intelligence",
  "customer-sentiment",
  "launch-readiness",
  "strategic-positioning",
  "battle-card",
  "mixed-other"
];
const VERTICAL_VALUES = ["ST", "HR", "FT", "OT"];
const STAGE_VALUES = ["series-a", "series-b-c", "series-d-plus"];
const GEO_VALUES = ["india", "apac", "mea", "us", "uk", "eu", "global"];
const ICP_VALUES = ["smb", "mid-market", "enterprise", "mixed"];

const JTBD_TO_SUFFIX = {
  "market-sizing": "01",
  "feature-gap-analysis": "02",
  "pricing-intelligence": "03",
  "customer-sentiment": "04",
  "launch-readiness": "05",
  "strategic-positioning": "06",
  "battle-card": "06"
};

function isFilled(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function normalizeWhitespace(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

function normalizeArray(arr) {
  if (!Array.isArray(arr)) return [];
  return arr.map((x) => normalizeWhitespace(x)).filter(Boolean);
}

function lower(value) {
  return normalizeWhitespace(value).toLowerCase();
}

function upper(value) {
  return normalizeWhitespace(value).toUpperCase();
}

function toTitleRole(role) {
  switch (role) {
    case "founder":
      return "Founder";
    case "pmm":
      return "PMM";
    case "sales-leader":
      return "Sales Leader";
    case "strategy":
      return "Strategy";
    default:
      return "inferred-other";
  }
}

function detectSellerRole(rawText) {
  const text = lower(rawText);
  if (/\b(founder|cofounder|co-founder|ceo)\b/.test(text)) return "founder";
  if (/\b(pmm|product marketing|product marketer|positioning lead|messaging lead)\b/.test(text)) return "pmm";
  if (/\b(sales leader|vp sales|head of sales|cro|revenue leader|sales director)\b/.test(text)) return "sales-leader";
  if (/\b(strategy|strategic planning|corp strategy|corporate strategy)\b/.test(text)) return "strategy";
  return "";
}

function detectExplicitCompany(rawText) {
  const text = normalizeWhitespace(rawText);
  const patterns = [
    /\b(?:at|from)\s+([A-Z][A-Za-z0-9&.\-]*(?:\s+[A-Z][A-Za-z0-9&.\-]*){0,3})\b/,
    /\b(?:company|product)\s+(?:called|named)?\s*([A-Z][A-Za-z0-9&.\-]*(?:\s+[A-Z][A-Za-z0-9&.\-]*){0,3})\b/,
    /\b(?:we are|i am with)\s+([A-Z][A-Za-z0-9&.\-]*(?:\s+[A-Z][A-Za-z0-9&.\-]*){0,3})\b/
  ];
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match && match[1]) {
      const candidate = normalizeWhitespace(match[1]);
      if (!/^(Series|India|US|UK|EU|APAC|MEA|Global)$/i.test(candidate) && !/^(sales tech|hr tech|fintech|ops tech)$/i.test(candidate)) {
        return candidate;
      }
    }
  }
  return "";
}

function detectPrimaryJtbd(rawText) {
  const text = lower(rawText);
  if (/\b(battlecard|battle card|objection handling|deal support|win loss|win\/loss)\b/.test(text)) return "battle-card";
  if (/\b(pricing|package|packaging|price point|discount)\b/.test(text)) return "pricing-intelligence";
  if (/\b(feature gap|feature-gap|gap analysis|compare features|feature comparison)\b/.test(text)) return "feature-gap-analysis";
  if (/\b(sentiment|reviews|review analysis|voice of customer|customer sentiment)\b/.test(text)) return "customer-sentiment";
  if (/\b(launch readiness|launch-ready|launch prep|launch against|are we ready)\b/.test(text)) return "launch-readiness";
  if (/\b(positioning|position|narrative|differentiat|message house|strategic positioning)\b/.test(text)) return "strategic-positioning";
  if (/\b(market size|market sizing|tam|sam|sizing)\b/.test(text)) return "market-sizing";
  if (/\b(competitor analysis|competitive analysis)\b/.test(text)) return "mixed-other";
  return "";
}

function detectVertical(rawText, competitors = []) {
  const text = lower(rawText);
  const joinedCompetitors = lower(competitors.join(" "));
  const corpus = `${text} ${joinedCompetitors}`;

  if (/\b(sales tech|crm|sales engagement|revenue intelligence|sales enablement|marketing automation|pipeline|apollo|outreach|salesloft|salesforce|hubspot|zoho)\b/.test(corpus)) {
    return "ST";
  }
  if (/\b(hr tech|hris|hcm|talent acquisition|rippling|deel|darwinbox)\b/.test(corpus)) {
    return "HR";
  }
  if (/\b(fintech|payments|payment orchestration|expense|spend management|digital banking|stripe|adyen|checkout\.com)\b/.test(corpus)) {
    return "FT";
  }
  if (/\b(ops tech|operations|workflow automation|project management|itsm|observability|devops|cybersecurity|crowdstrike|sentinelone|microsoft)\b/.test(corpus)) {
    return "OT";
  }
  return "";
}

function detectScenarioId(rawText, vertical, jtbd) {
  const explicit = normalizeWhitespace(rawText).match(/\b(ST|HR|FT|OT)-0[1-6]\b/i);
  if (explicit) return explicit[0].toUpperCase();

  if (!vertical || !jtbd) return "";
  const suffix = JTBD_TO_SUFFIX[jtbd];
  if (!suffix) return "";
  return `${vertical}-${suffix}`;
}

function detectStage(rawText) {
  const text = lower(rawText);
  if (/\bseries a\b/.test(text)) return "series-a";
  if (/\bseries b\b|\bseries c\b|\bseries b-c\b/.test(text)) return "series-b-c";
  if (/\bseries d\b|\bseries e\b|\bseries f\b|\bseries d\+\b|\bseries-d-plus\b/.test(text)) return "series-d-plus";
  return "";
}

function detectGeography(rawText) {
  const text = lower(rawText);
  if (/\bindia\b/.test(text)) return "india";
  if (/\bapac\b/.test(text)) return "apac";
  if (/\bmea\b/.test(text)) return "mea";
  if (/\bus\b|\busa\b|\bunited states\b/.test(text)) return "us";
  if (/\buk\b|\bunited kingdom\b/.test(text)) return "uk";
  if (/\beu\b|\beurope\b/.test(text)) return "eu";
  if (/\bglobal\b/.test(text)) return "global";
  return "";
}

function detectIcp(rawText) {
  const text = lower(rawText);
  if (/\bmid-market\b|\bmid market\b/.test(text)) return "mid-market";
  if (/\benterprise\b/.test(text)) return "enterprise";
  if (/\bsmb\b|\bsmall business\b/.test(text)) return "smb";
  if (/\bmixed\b/.test(text)) return "mixed";
  return "";
}

function splitCompetitorList(candidate) {
  return normalizeWhitespace(candidate)
    .replace(/\band\b/gi, ",")
    .split(",")
    .map((item) => normalizeWhitespace(item))
    .filter((item) => item.length > 1);
}

function detectCompetitors(rawText) {
  const text = normalizeWhitespace(rawText);
  const patterns = [
    /\b(?:against|versus|vs\.?|compete with)\s+(.+?)(?=\s+\b(before|for|in|by|with|need|help|tomorrow|next|within)\b|[.!?]|$)/i
  ];
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match && match[1]) {
      return splitCompetitorList(match[1]).slice(0, 5);
    }
  }
  return [];
}

function detectObjective(rawText, jtbd) {
  const text = normalizeWhitespace(rawText);
  if (!text) return "";
  if (jtbd === "pricing-intelligence") return `Make a pricing decision based on competitive pricing intelligence: ${text}`;
  if (jtbd === "feature-gap-analysis") return `Identify the most material feature gaps versus competitors: ${text}`;
  if (jtbd === "customer-sentiment") return `Synthesize customer sentiment to guide a competitive decision: ${text}`;
  if (jtbd === "launch-readiness") return `Assess launch readiness versus competitors: ${text}`;
  if (jtbd === "strategic-positioning") return `Sharpen strategic positioning against named competitors: ${text}`;
  if (jtbd === "battle-card") return `Prepare a competitor battlecard to support live selling: ${text}`;
  if (jtbd === "market-sizing") return `Estimate market size and implications for the decision: ${text}`;
  return text;
}

function detectDeadline(rawText) {
  const text = normalizeWhitespace(rawText);
  const patterns = [
    /\bnext\s+[A-Z][a-z]+\b/i,
    /\btomorrow\b/i,
    /\b\d+\s+days?\b/i,
    /\b\d+\s+weeks?\b/i,
    /\bnext\s+month\b/i,
    /\bnext\s+quarter\b/i,
    /\bwithin\s+\d+\s+days?\b/i,
    /\bwithin\s+\d+\s+weeks?\b/i
  ];
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) return normalizeWhitespace(match[0]);
  }
  return "";
}

function inferVerticalFromScenarioId(scenarioId) {
  const match = String(scenarioId || "").toUpperCase().match(/^(ST|HR|FT|OT)-0[1-6]$/);
  return match ? match[1] : "";
}

function inferJtbdFromScenarioId(scenarioId) {
  const id = String(scenarioId || "").toUpperCase();
  const suffix = id.split("-")[1];
  switch (suffix) {
    case "01":
      return "market-sizing";
    case "02":
      return "feature-gap-analysis";
    case "03":
      return "pricing-intelligence";
    case "04":
      return "customer-sentiment";
    case "05":
      return "launch-readiness";
    case "06":
      return "strategic-positioning";
    default:
      return "";
  }
}

function normalizeCompetitiveRequest(raw) {
  const userInput = normalizeWhitespace(raw.userInput || "");
  const sellerRole = isFilled(raw.sellerRole) ? lower(raw.sellerRole) : detectSellerRole(userInput);
  const company = isFilled(raw.company) ? normalizeWhitespace(raw.company) : detectExplicitCompany(userInput);
  const explicitScenarioId = isFilled(raw.scenarioId) ? upper(raw.scenarioId) : "";
  const primaryJtbd = isFilled(raw.primaryJtbd)
    ? lower(raw.primaryJtbd)
    : detectPrimaryJtbd(userInput) || inferJtbdFromScenarioId(explicitScenarioId);
  const topCompetitors = normalizeArray(raw.topCompetitors).length > 0 ? normalizeArray(raw.topCompetitors) : detectCompetitors(userInput);
  const vertical = isFilled(raw.vertical)
    ? upper(raw.vertical)
    : detectVertical(userInput, topCompetitors) || inferVerticalFromScenarioId(explicitScenarioId);
  const scenarioId = explicitScenarioId || detectScenarioId(userInput, vertical, primaryJtbd);
  const companyStage = isFilled(raw.companyStage) ? lower(raw.companyStage) : detectStage(userInput);
  const primaryGeography = isFilled(raw.primaryGeography) ? lower(raw.primaryGeography) : detectGeography(userInput);
  const icpSegment = isFilled(raw.icpSegment) ? lower(raw.icpSegment) : detectIcp(userInput);
  const objective = isFilled(raw.objective) ? normalizeWhitespace(raw.objective) : detectObjective(userInput, primaryJtbd);
  const deadline = isFilled(raw.deadline) ? normalizeWhitespace(raw.deadline) : detectDeadline(userInput);
  const availableEvidence = isFilled(raw.availableEvidence) ? normalizeWhitespace(raw.availableEvidence) : "";
  const knownConstraints = isFilled(raw.knownConstraints) ? normalizeWhitespace(raw.knownConstraints) : "";

  return {
    userInput,
    sellerRole,
    company,
    primaryJtbd,
    vertical,
    scenarioId,
    companyStage,
    primaryGeography,
    icpSegment,
    topCompetitors,
    objective,
    deadline,
    availableEvidence,
    knownConstraints
  };
}

function pickFirstMissing(input) {
  if (!isFilled(input.sellerRole)) return "sellerRole";
  if (!isFilled(input.company)) return "company";
  if (!isFilled(input.primaryJtbd)) return "primaryJtbd";
  if (!isFilled(input.vertical)) return "vertical";
  if (!isFilled(input.scenarioId)) return "scenarioId";
  if (!Array.isArray(input.topCompetitors) || input.topCompetitors.length === 0) return "topCompetitors";
  if (!isFilled(input.primaryGeography)) return "primaryGeography";
  if (!isFilled(input.icpSegment)) return "icpSegment";
  if (!isFilled(input.companyStage)) return "companyStage";
  if (!isFilled(input.objective)) return "objective";
  if (!isFilled(input.deadline)) return "deadline";
  return null;
}

function clarificationQuestion(field) {
  switch (field) {
    case "sellerRole":
      return "What is your seller role for this decision: Founder, PMM, Sales Leader, or Strategy?";
    case "company":
      return "Which company or product should I anchor this analysis on?";
    case "primaryJtbd":
      return "What do you need most right now: pricing, feature gaps, launch readiness, customer sentiment, positioning, or a battlecard?";
    case "vertical":
      return "Is your primary decision about revenue execution, people operations, financial rails, or operational reliability?";
    case "scenarioId":
      return "Which scenario should I run: market sizing, feature gaps, pricing, customer sentiment, launch readiness, or positioning?";
    case "topCompetitors":
      return "Which competitors matter most for this decision?";
    case "primaryGeography":
      return "Which geography should I optimize this analysis for?";
    case "icpSegment":
      return "Are you selling mainly to SMB, mid-market, enterprise, or a mixed ICP?";
    case "companyStage":
      return "What stage is the company: series-a, series-b-c, or series-d-plus?";
    case "objective":
      return "What is the primary decision you need to make with this analysis?";
    case "deadline":
      return "What is the deadline or planning horizon for this decision?";
    default:
      return "What is the missing input I should anchor on?";
  }
}

function computeFreePremiumStage(input) {
  const text = lower(input.userInput);
  if (/\b(export-ready|export ready|deck|team-ready|team ready|implementation workflow|execution workspace|recurring monitoring|recurring tracking|workspace)\b/.test(text)) {
    return "premium-requested";
  }
  return "free-diagnostic";
}

function computeConfidence(input) {
  if (isFilled(input.availableEvidence)) return "High";
  return "Medium";
}

function ownerForRole(role) {
  switch (role) {
    case "founder":
      return "Founder";
    case "pmm":
      return "PMM";
    case "sales-leader":
      return "Sales Leader";
    case "strategy":
      return "Strategy";
    default:
      return "Decision owner";
  }
}

function actionPanelForJtbd(jtbd, owner) {
  switch (jtbd) {
    case "pricing-intelligence":
      return {
        h24: [
          `Inventory public pricing pages and packaging for the named competitors (${owner})`,
          `Lock the price-to-value comparison frame before more research sprawl starts (${owner})`,
          `Define the pricing claims that require external validation (${owner})`
        ],
        d7: [
          `Build a competitor pricing matrix with list, packaging, and discount signals (${owner})`,
          `Pressure-test negotiation assumptions against public evidence (${owner})`,
          `Draft the pricing narrative leadership can use internally and externally (${owner})`
        ],
        d30: [
          `Refine pricing recommendations against buyer segment response (${owner})`,
          `Validate commercial friction and hidden-cost assumptions (${owner})`,
          `Convert the pricing read into a field-ready artifact (${owner})`
        ]
      };
    case "launch-readiness":
      return {
        h24: [
          `Lock the launch objective, competitor scope, and proof-point gaps (${owner})`,
          `Audit the launch narrative against the named threats (${owner})`,
          `Identify the readiness risks that could derail the launch (${owner})`
        ],
        d7: [
          `Build a launch readiness scorecard against named competitors (${owner})`,
          `Pressure-test pricing, proof, and enablement readiness (${owner})`,
          `Decide whether to narrow the launch scope or sharpen the message (${owner})`
        ],
        d30: [
          `Run pre-launch validation with customer proof and field feedback (${owner})`,
          `Tighten objections, talk tracks, and launch sequencing (${owner})`,
          `Turn the scorecard into a team-ready execution brief (${owner})`
        ]
      };
    case "strategic-positioning":
    case "battle-card":
      return {
        h24: [
          `Lock the positioning frame and named competitive wedge (${owner})`,
          `Strip out any unsupported comparative claims before field use (${owner})`,
          `Define the talk tracks that matter most for the target buyer (${owner})`
        ],
        d7: [
          `Draft a message house and competitor rebuttal grid (${owner})`,
          `Validate the strongest proof points and weakest claims (${owner})`,
          `Turn the positioning into a battlecard-ready structure (${owner})`
        ],
        d30: [
          `Pressure-test the message in live conversations (${owner})`,
          `Refine the claim hierarchy based on objection patterns (${owner})`,
          `Operationalize the positioning into repeatable enablement (${owner})`
        ]
      };
    case "feature-gap-analysis":
      return {
        h24: [
          `Define the product capabilities that matter most in this decision (${owner})`,
          `Lock the competitor comparison criteria before expanding scope (${owner})`,
          `List the evidence needed to validate product claims (${owner})`
        ],
        d7: [
          `Build the feature matrix with explicit confidence tags (${owner})`,
          `Separate meaningful gaps from irrelevant feature noise (${owner})`,
          `Draft recommended response options by gap severity (${owner})`
        ],
        d30: [
          `Validate the feature gaps with customer and market evidence (${owner})`,
          `Prioritize response by revenue impact, not by feature count (${owner})`,
          `Convert the matrix into a decision-ready artifact (${owner})`
        ]
      };
    case "customer-sentiment":
      return {
        h24: [
          `Lock the review sources and competitor scope (${owner})`,
          `Define the buyer themes that matter most (${owner})`,
          `Separate anecdote from repeatable sentiment signal (${owner})`
        ],
        d7: [
          `Synthesize sentiment themes by competitor (${owner})`,
          `Map sentiment into product, pricing, and GTM implications (${owner})`,
          `Draft the key risk and opportunity narrative (${owner})`
        ],
        d30: [
          `Validate themes against more recent evidence (${owner})`,
          `Translate sentiment into product and messaging actions (${owner})`,
          `Operationalize sentiment monitoring into a repeatable workflow (${owner})`
        ]
      };
    case "market-sizing":
      return {
        h24: [
          `Lock the market definition and category boundary (${owner})`,
          `Define the sizing method and assumptions (${owner})`,
          `List the evidence gaps that could distort the estimate (${owner})`
        ],
        d7: [
          `Build a first-pass TAM/SAM/SOM view (${owner})`,
          `Test the assumptions against geography and ICP realities (${owner})`,
          `Draft the sizing implications for the decision (${owner})`
        ],
        d30: [
          `Refine the sizing model with additional evidence (${owner})`,
          `Pressure-test the result against competitor scale signals (${owner})`,
          `Convert the sizing view into a board-usable brief (${owner})`
        ]
      };
    default:
      return {
        h24: [
          `Lock the decision scope and missing evidence plan (${owner})`,
          `Confirm the competitor list and scenario fit (${owner})`,
          `Prevent analysis sprawl by agreeing the evaluation frame (${owner})`
        ],
        d7: [
          `Build the first structured competitor comparison (${owner})`,
          `Test the strongest assumptions before recommending action (${owner})`,
          `Draft the decision memo with explicit risks (${owner})`
        ],
        d30: [
          `Refine the analysis with better evidence (${owner})`,
          `Operationalize the strongest recommendation (${owner})`,
          `Create a repeatable review cadence (${owner})`
        ]
      };
  }
}

function mediumLongTerm(owner) {
  return {
    d60: [
      `Pressure-test the recommendation against new evidence (${owner})`,
      `Tighten the field narrative and validation plan (${owner})`,
      `Close remaining confidence gaps before major execution bets (${owner})`
    ],
    d90: [
      `Operationalize the selected response path (${owner})`,
      `Install a recurring competitor review rhythm (${owner})`,
      `Track execution outcomes against the original decision logic (${owner})`
    ],
    medium: [
      `Build a repeatable CI operating cadence with named owners (${owner})`,
      `Move from one-off analysis to scenario-based decision support (${owner})`
    ],
    long: [
      `Institutionalize CI as a discipline across pricing, positioning, and launch decisions (${owner})`,
      `Create a durable source-of-truth workflow for competitor intelligence (${owner})`
    ]
  };
}

function renderBulletLines(items) {
  return items.map((item) => `- ${item}`).join("\n");
}

function buildArtifactBlock(card, input) {
  const artifactLine = card?.scenarioArtifact || `Scenario-specific artifact for ${input.scenarioId}`;
  return `- ${artifactLine}`;
}

function buildSourcesAndAssumptions(input, card) {
  const sources = [
    "user-provided conversational inputs",
    "chatgpt/INPUT_CONTRACT.md",
    "chatgpt/OUTPUT_SCHEMA.md",
    "chatgpt/TAXONOMY_STANDARD.md",
    "chatgpt/SCENARIO_INDEX.md"
  ];
  if (card) {
    sources.push(`scenarios/${input.scenarioId}.md`);
  }
  const assumptions = [];
  if (!isFilled(input.availableEvidence)) {
    assumptions.push("No external evidence has been supplied yet; confidence remains Medium.");
  }
  if (!isFilled(input.knownConstraints)) {
    assumptions.push("No additional constraints were provided.");
  }
  if (assumptions.length === 0) {
    assumptions.push("No non-critical assumptions remain open.");
  }

  return {
    sources,
    assumptions
  };
}

function buildSubstantiveOutput(input) {
  const card = SCENARIO_CARDS[input.scenarioId];
  const confidence = computeConfidence(input);
  const premiumStage = computeFreePremiumStage(input);
  const owner = ownerForRole(input.sellerRole);
  const actionPanel = actionPanelForJtbd(input.primaryJtbd, owner);
  const longerHorizon = mediumLongTerm(owner);
  const scenarioTitle = card?.title || input.scenarioId;
  const typicalBuyer = card?.typicalBuyer || "Buyer context not found in scenario card";
  const lens = card?.analysisLens || [];
  const constraints = card?.constraints || [];
  const sourcesAndAssumptions = buildSourcesAndAssumptions(input, card);
  const handoffAvailable = String(process.env.GTMHELIX_HANDOFF_AVAILABLE || "true").toLowerCase() !== "false";

  const competitorSnapshotLines = input.topCompetitors.map(
    (competitor) => `- ${competitor} | high relevance | medium threat | named by user for this decision | ${confidence}`
  );

  const riskLines = [
    "- Thin external evidence | Medium | Validate with first-party and public signals before execution | Medium",
    "- Scenario mismatch risk | Medium | Confirm scenario fit against the stated objective | Medium",
    "- Competitor scope drift | Medium | Keep the analysis anchored to the named competitors first | Medium"
  ];

  const handoffSection =
    premiumStage === "premium-requested"
      ? handoffAvailable
        ? [
            "- diagnostic work completed: normalization, routing, competitor anchoring, and scenario framing",
            "- why next step belongs on GTMHelix.com: the request is now export-heavy, workflow-heavy, or execution-heavy",
            "- what unlocks on GTMHelix.com: detailed teardown, team-ready artifacts, recurring tracking, and execution workflows"
          ]
        : [
            "- GTMHelix.com handoff is not available right now.",
            "- Continuing inside ChatGPT with the best available end-to-end workflow."
          ]
      : [
          "- completed: normalization, routing, competitor anchoring, and scenario framing",
          "- remains inside free diagnostic layer: evidence-backed comparative analysis and scenario artifact refinement",
          "- premium handoff trigger next: export-ready pack, recurring monitoring, team-ready artifacts, or implementation workflow"
        ];

  const keySignalsLines = [
    `- Pricing signals: ${input.primaryJtbd === "pricing-intelligence" ? "price, packaging, and discount posture are priority validation areas" : "pricing is secondary unless the scenario specifically requires it"}`,
    `- Product / feature signals: focus on the scenario lens for ${scenarioTitle.toLowerCase()}`,
    `- GTM signals: evaluate competitor messaging, motion, and buyer-fit implications`,
    `- Buyer / category signals: anchored to ${input.icpSegment} in ${input.primaryGeography}; typical buyer context = ${typicalBuyer}`
  ];

  const recommendationsLines = [
    `- owner: ${owner} | expected outcome: lock the evaluation frame for ${scenarioTitle.toLowerCase()} | confidence: ${confidence} | what must be validated next: first-party and public evidence`,
    `- owner: ${owner} | expected outcome: convert the named competitors into a scenario-specific comparative artifact | confidence: ${confidence} | what must be validated next: claims, gaps, and constraints from market evidence`,
    `- owner: ${owner} | expected outcome: produce a decision-ready brief without unsupported claims | confidence: ${confidence} | what must be validated next: assumptions and risk exposure`
  ];

  const contextLines = [
    `- inferred or confirmed company context: ${input.company}, ${input.companyStage}, ${input.primaryGeography}, ${input.icpSegment}`,
    `- confirmed objective: ${input.objective}`,
    `- explicit constraints: ${isFilled(input.knownConstraints) ? input.knownConstraints : "no known constraints provided"}`,
    `- explicit evidence provided: ${isFilled(input.availableEvidence) ? input.availableEvidence : "user-provided company, role, competitors, and decision framing only"}`,
    `- explicit assumptions made: ${sourcesAndAssumptions.assumptions.join(" ")}`,
    `- explicit missing-but-non-blocking items, if any: none`
  ];

  const output = [
    "## 0) Output Header",
    `- **Vertical Route:** ${input.vertical} (confidence: ${confidence})`,
    `- **Scenario Route:** ${input.scenarioId} - ${scenarioTitle}`,
    `- **Primary JTBD:** ${input.primaryJtbd}`,
    `- **Seller Role Lens:** ${toTitleRole(input.sellerRole)}`,
    `- **Company:** ${input.company}`,
    `- **Free/Premium Stage:** ${premiumStage}`,
    "",
    "## 1) Action Panel",
    renderBulletLines(actionPanel.h24.map((x) => `**Do in 24h**: ${x}`)).replace(/^- \*\*Do in 24h\*\*:/m, "- **Do in 24h**:"),
    renderBulletLines(actionPanel.d7.map((x) => `**Do in 7d**: ${x}`)).replace(/^- \*\*Do in 7d\*\*:/m, "- **Do in 7d**:"),
    renderBulletLines(actionPanel.d30.map((x) => `**Do in 30d**: ${x}`)).replace(/^- \*\*Do in 30d\*\*:/m, "- **Do in 30d**:"),
    renderBulletLines(longerHorizon.d60.map((x) => `**Do in 60d**: ${x}`)).replace(/^- \*\*Do in 60d\*\*:/m, "- **Do in 60d**:"),
    renderBulletLines(longerHorizon.d90.map((x) => `**Do in 90d**: ${x}`)).replace(/^- \*\*Do in 90d\*\*:/m, "- **Do in 90d**:"),
    renderBulletLines(longerHorizon.medium.map((x) => `**Medium term**: ${x}`)).replace(/^- \*\*Medium term\*\*:/m, "- **Medium term**:"),
    renderBulletLines(longerHorizon.long.map((x) => `**Long term**: ${x}`)).replace(/^- \*\*Long term\*\*:/m, "- **Long term**:"),
    "",
    "## 2) Executive Summary",
    `- Context recap: ${input.company} is evaluating ${scenarioTitle.toLowerCase()} in ${input.primaryGeography} for a ${input.companyStage} company selling to ${input.icpSegment}.`,
    `- Decision recommendation: proceed with a disciplined, evidence-backed ${scenarioTitle.toLowerCase()} review anchored on the named competitors.`,
    `- Why this matters now: the decision horizon is ${input.deadline}, so discipline and routing matter more than generic advisory output.`,
    "",
    "## 3) JTBD and Context Normalization",
    ...contextLines,
    "",
    "## 4) Competitor Snapshot",
    ...competitorSnapshotLines,
    "",
    "## 5) Key Signals",
    ...keySignalsLines,
    ...(lens.length > 0 ? [`- Scenario lens: ${lens.join("; ")}`] : []),
    "",
    "## 6) Recommendations",
    ...recommendationsLines,
    "",
    "## 7) Risks and Validation Needs",
    ...riskLines,
    ...(constraints.length > 0 ? [`- Scenario constraints: ${constraints.join("; ")} | Medium | keep claims inside the scenario card guardrails | Medium`] : []),
    "",
    "## 8) Deliverable Artifact",
    buildArtifactBlock(card, input),
    "",
    "## 9) Handoff Decision",
    ...handoffSection,
    "",
    "## 10) Sources and Assumptions",
    `- explicit source list: ${sourcesAndAssumptions.sources.join("; ")}`,
    `- explicit assumptions list: ${sourcesAndAssumptions.assumptions.join(" ")}`,
    `- explicit confidence summary: ${confidence} = ${confidence === "High" ? "evidence and routing are strong enough to act now" : "usable now, but named validations are still required"}`
  ].join("\n");

  return output;
}

function createServer() {
  const server = new McpServer({
    name: "gtm-helix-competitive-intelligence-copilot",
    version: "3.0.0"
  });

  server.tool(
    "health_check",
    "Health check for the CI MCP server",
    {},
    async () => {
      const scenarioCount = Object.keys(SCENARIO_CARDS).length;
      return {
        content: [
          {
            type: "text",
            text: `MCP server is running. Scenario cards loaded: ${scenarioCount}. Docs loaded: ${Object.keys(DOCS).length}.`
          }
        ]
      };
    }
  );

  server.tool(
    "competitive_scenario",
    "Run a repo-aware competitive intelligence scenario with deterministic routing and strict clarification gates",
    {
      userInput: z.string().optional().describe("Conversational user input"),
      sellerRole: z.string().optional().describe("Seller role override"),
      company: z.string().optional().describe("Company or product override"),
      primaryJtbd: z.string().optional().describe("Primary JTBD override"),
      vertical: z.string().optional().describe("Vertical override"),
      scenarioId: z.string().optional().describe("Scenario ID override"),
      companyStage: z.string().optional().describe("Company stage override"),
      primaryGeography: z.string().optional().describe("Primary geography override"),
      icpSegment: z.string().optional().describe("ICP segment override"),
      topCompetitors: z.array(z.string()).optional().describe("Top competitors override"),
      objective: z.string().optional().describe("Objective override"),
      deadline: z.string().optional().describe("Deadline override"),
      availableEvidence: z.string().optional().describe("Available evidence"),
      knownConstraints: z.string().optional().describe("Known constraints")
    },
    async (raw) => {
      const input = normalizeCompetitiveRequest(raw);
      const missing = pickFirstMissing(input);

      if (missing) {
        return {
          content: [
            {
              type: "text",
              text: clarificationQuestion(missing)
            }
          ]
        };
      }

      const output = buildSubstantiveOutput(input);
      return {
        content: [
          {
            type: "text",
            text: output
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
  res.status(200).json({
    ok: true,
    scenarioCardsLoaded: Object.keys(SCENARIO_CARDS).length,
    docsLoaded: Object.keys(DOCS).length
  });
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
  try {
    if (!sessionId || !sessions.has(sessionId)) {
      return res.status(400).json({ error: "Invalid or missing sessionId" });
    }

    const { transport } = sessions.get(sessionId);
    await transport.handlePostMessage(req, res);
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
