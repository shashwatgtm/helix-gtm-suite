# Notion Integration Reference

## Connection Setup

### MCP Connector (Claude.ai)
User connects via Settings → Connectors → Notion. The connector handles authentication and page access.

### API Integration (Custom implementations)
1. Create integration at notion.so/my-integrations
2. Get the Internal Integration Token
3. User must share specific pages/databases with the integration (Notion requires explicit sharing)
4. Use token in Authorization header: `Bearer {token}`

### Manual Mode
Ask user: "Share a link to your tasks database or paste your to-do list."

## Required Capabilities

```
Read content         - Read pages and databases
Read comments        - Read page comments  
Read user info       - Get workspace members
```

## API Patterns

### Fetch User's Tasks

```
APPROACH 1: Query database with filter
POST /databases/{database_id}/query
{
  "filter": {
    "and": [
      {"property": "Assignee", "people": {"contains": "{user_id}"}},
      {"property": "Status", "status": {"does_not_equal": "Done"}}
    ]
  },
  "sorts": [
    {"property": "Due Date", "direction": "ascending"}
  ]
}

APPROACH 2: Search all accessible
POST /search
{
  "query": "",
  "filter": {"property": "object", "value": "page"},
  "sort": {"direction": "descending", "timestamp": "last_edited_time"}
}
Then filter client-side for assigned tasks.
```

### Task Status Detection

Common status values:
- Not Started / To Do / Backlog
- In Progress / Working / Active
- Blocked / Waiting / On Hold — flag these
- In Review / Pending Approval — flag if user is approver
- Done / Complete / Shipped

### Due Date Logic

```python
today = current_date()
this_week = today + timedelta(days=7)

BUCKETS:
- OVERDUE: due_date < today
- TODAY: due_date == today
- THIS_WEEK: today < due_date <= this_week
- LATER: due_date > this_week
```

### Blocker Detection

```
CHECK FOR BLOCKERS:
1. Status == "Blocked" or "Waiting"
2. Property named "Blocker" or "Blocked By" has value
3. Comments contain "blocked", "waiting on", "need"
4. Linked items (relations) have incomplete dependencies

ENRICH BLOCKED TASKS:
- Who/what is blocking?
- How long has it been blocked?
- Is there a Slack thread about it?
```

## Entity Extraction for Slack Matching

Extract from Notion: task titles, project names (from project relation), client names (from client relation or property), assignee names (for "involves direct report" matching), tags/labels.

Use for: "Should know" thread detection in Slack.

## Error Handling

```
401 Unauthorized  → Token expired, prompt re-auth
403 Forbidden     → Page not shared with integration
404 Not Found     → Database/page deleted or moved
429 Rate Limit    → Wait 1 second, retry (3 max)
```

## Common Database Patterns

### Task Database

```
EXPECTED PROPERTIES:
- Title (title)
- Status (status/select)
- Assignee (people)
- Due Date (date)
- Priority (select: High/Medium/Low)
- Project (relation)
- Client (relation or select)
- Blockers (rich_text or relation)
```

### Project Database

```
EXPECTED PROPERTIES:
- Name (title)
- Status (status)
- Owner (people)
- Client (relation)
- Start/End Dates (date)
- Related Tasks (relation)
```

Adapt to actual schema discovered via database query.
