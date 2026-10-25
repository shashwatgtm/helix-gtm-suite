# Email Integration Reference

## Connection Setup

### MCP Connector (Claude.ai)
User connects via Settings → Connectors → Gmail (or Outlook). No action needed from the skill.

### OAuth (Custom implementations)
- Gmail: Google OAuth 2.0 with `gmail.readonly` scope
- Outlook: Microsoft Graph API with `Mail.Read` scope
- Generic IMAP: Username/password or app-specific password (limited features)

### Manual Mode
Ask user: "Forward any internal emails that need a response, or list the subjects."

## Supported Providers

```
- Gmail (Google Workspace)
- Microsoft Outlook/365
- Generic IMAP (limited features)
```

## Core Filtering Logic

### Domain Filter

```
INCLUDE ONLY: Emails from company's own domain(s)
DETECT COMPANY DOMAIN: 
  1. From user's email address
  2. From calendar/profile settings
  3. Ask once if unclear

MULTI-DOMAIN COMPANIES:
- Store list: ["company.com", "company.io", "acquired-brand.com"]
```

### Recipient Position Filter

| Position | Priority | Include? |
|----------|----------|----------|
| TO: user (direct) | HIGH | Always |
| TO: user + response requested | HIGH | Always |
| CC: user + response requested | MEDIUM | If response requested |
| CC: user only | LOW | Skip unless urgent |
| BCC: user | LOW | Skip |

### Response Request Detection

```python
RESPONSE_SIGNALS = [
    # Direct asks
    r"please respond", r"please reply", r"let me know",
    r"your thoughts\?", r"your input", r"need your",
    r"can you", r"could you", r"would you",
    
    # Questions directed at user
    r"@{user_name}.*\?",
    
    # Deadline indicators
    r"by (EOD|end of day|tomorrow|monday|friday)",
    r"deadline.*\d{1,2}[/-]\d{1,2}",
    
    # Explicit CC reasoning
    r"cc'ing you (for|to)", r"adding you (for|to)"
]

CHECK: If user is CC'd, only include if response signals found
```

### Bulk/Digest Exclusion

```
EXCLUDE PATTERNS:

HEADER CHECKS:
- List-Unsubscribe header present
- Precedence: bulk or list
- X-Mailer indicates newsletter tool
- X-Campaign-ID present

SENDER PATTERNS:
- noreply@, no-reply@, notifications@
- digest@, updates@, alerts@
- *-noreply@company.com

SUBJECT PATTERNS:
- "[Digest]", "[Weekly]", "[Daily]"
- "Newsletter", "Roundup", "Summary"
- Automated tool patterns: "[JIRA]", "[GitHub]", "[Confluence]"

EXCEPTION: Include automated emails IF:
- Subject contains "urgent", "critical", "failed", "error"
- User is directly addressed in body
```

## Email Analysis

### Key Information Extraction

```
For each qualifying email, extract:
- Sender: Name + role (from signature or directory)
- Subject: Full subject line
- Key Ask: First action item or question
- Deadline: Any mentioned deadline
- Thread Length: How many replies
- Attachments: Note if present (don't fetch)
- Urgency Signals: Keywords, formatting (!!)
```

### Thread Summarization

```
FOR EMAIL THREADS (>2 messages):
1. Read most recent 3 messages
2. Identify: What's resolved vs. open
3. Extract: Current status, what's needed from user
4. Note: How long thread has been active
```

## Gmail-Specific

```
SEARCH QUERY:
q=to:me OR cc:me 
  is:unread 
  after:{last_briefing_timestamp}
  -category:promotions 
  -category:social 
  -category:updates
  from:*@company.com

LABELS TO SKIP:
- [Gmail]/Spam
- [Gmail]/Trash
- Newsletters (if user has label)
```

## Outlook-Specific

```
GRAPH API FILTER:
$filter=
  receivedDateTime ge {last_briefing} and
  (toRecipients/any(r: r/emailAddress/address eq '{user_email}') or
   ccRecipients/any(r: r/emailAddress/address eq '{user_email}')) and
  from/emailAddress/address endswith '@company.com'

EXCLUDE FOLDERS:
- Junk Email
- Deleted Items
- Clutter
```

## Error Handling

```
401 Unauthorized  → Token expired, re-auth
403 Forbidden     → Scope missing (mail.read)
429 Rate Limit    → Back off, show partial results
Timeout           → "Email fetch slow, continuing with other sources"
```
