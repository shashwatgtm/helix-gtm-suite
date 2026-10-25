# Slack Integration Reference

## Connection Setup

### MCP Connector (Claude.ai)
User connects via Settings → Connectors → Slack. No action needed from the skill—just use the connector tools when available.

### OAuth (Custom implementations)
Create a Slack app at api.slack.com/apps with the scopes below. Use OAuth 2.0 flow. Store tokens securely with refresh handling.

### Manual Mode
If no API access, ask user: "Paste any Slack threads that might need my attention" or "Share a Slack export."

## Required Scopes

```
channels:history    - Read public channel messages
channels:read       - List channels
groups:history      - Read private channel messages  
groups:read         - List private channels
im:history          - Read DMs
im:read             - List DMs
mpim:history        - Read group DMs
search:read         - Search messages
users:read          - Get user info
users:read.email    - Get user emails
```

## API Patterns

### Fetch Mentions

```
METHOD: conversations.history + search.messages
QUERY: "from:@user OR to:@user"
PARAMS:
  - oldest: [timestamp of last briefing]
  - inclusive: true
  - limit: 100
```

### Fetch Thread Context

```
METHOD: conversations.replies
PARAMS:
  - channel: [channel_id]
  - ts: [thread_ts]
  - inclusive: true
  - limit: 200
  
NOTE: Always fetch FULL thread, not just the mention
```

### Channel Monitoring

```
DEFAULT MONITOR CHANNELS:
- #general, #urgent, #leadership, #all-hands
- Any channel with "alert", "escalation" in name
- User's team channel (detect from user profile)

EXCLUDE:
- #random, #watercooler, #social
- Channels with >1000 messages/day (too noisy)
```

## Thread Classification

### Urgency Signals

```python
URGENT_KEYWORDS = [
    "urgent", "asap", "blocker", "blocked", "critical",
    "escalate", "help needed", "dropping", "fire",
    "customer complaint", "churn", "cancel"
]

DEADLINE_PATTERNS = [
    r"by EOD", r"by end of day", r"need.*today",
    r"deadline.*\d{1,2}[/-]\d{1,2}", r"due.*\d{1,2}[/-]\d{1,2}"
]

FYI_SIGNALS = [
    "fyi", "no action", "just sharing", "heads up only",
    "no response needed", "for awareness"
]
```

### Tone Detection

```
FORMAL INDICATORS:
- "Dear", "Regarding", proper punctuation
- No emoji, no casual abbreviations
- Longer sentences, complete grammar

CASUAL INDICATORS:
- Emoji usage, "hey", "thanks!"
- Abbreviations: "thx", "lmk", "btw"
- Short sentences, fragments OK

MATCH OUTPUT TONE TO THREAD TONE
```

## Error Handling

```
401 Unauthorized → Token expired, prompt re-auth
403 Forbidden    → Missing scopes, list required ones
429 Rate Limit   → Wait and retry (respect Retry-After header)
Timeout          → Note "Slack slow to respond", continue with cached data if available
```

## "Should Know" Thread Detection

```
SIGNAL MATCHING ALGORITHM:

1. Extract entities from user's Notion tasks:
   - Client names
   - Project names
   - Deal names
   - Key stakeholders

2. For each thread in monitored channels:
   - Check if any entity appears in thread
   - Check if thread involves user's direct reports
   - Check for urgency keywords
   - Score based on signal count

3. Confidence threshold:
   - HIGH (3+ signals): Always include
   - MEDIUM (2 signals): Include with brief context
   - LOW (1 signal): Skip unless <2 hours old
```
