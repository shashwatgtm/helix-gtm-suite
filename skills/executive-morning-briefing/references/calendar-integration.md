# Calendar Integration Reference

## Connection Setup

### MCP Connector (Claude.ai)
User connects via Settings → Connectors → Google Calendar (or Outlook). No action needed from the skill.

### OAuth (Custom implementations)
- Google Calendar: Use Google OAuth 2.0 with `calendar.readonly` scope
- Outlook: Use Microsoft Graph API with `Calendars.Read` scope
- CalDAV: Basic auth or app-specific password

### Manual Mode
Ask user: "Share your calendar for today—screenshot, list of meetings, or paste from your calendar app."

## Supported Providers

```
- Google Calendar (primary)
- Microsoft Outlook/365
- Apple Calendar (via CalDAV)
```

## API Patterns (Google Calendar)

### Fetch Events

```
GET /calendars/{calendarId}/events
PARAMS:
  timeMin: [start of today, user timezone]
  timeMax: [end of tomorrow]
  singleEvents: true
  orderBy: startTime
```

### Detect Timezone

```
GET /users/me/settings/timezone
RETURNS: IANA timezone string (e.g., "Asia/Kolkata")

FALLBACK: Parse from first calendar event's timezone
LAST RESORT: Ask user once, remember
```

### Detect OOO Status

```
CHECK FOR:
1. All-day event with "OOO", "Out of Office", "PTO", "Vacation" in title
2. Event with outOfOffice eventType (Google-specific)
3. Working location set to "Out of office"
4. Status showing "outOfOffice" in free/busy

IF DETECTED:
- Extract return date from event end
- Prompt: "You're OOO until [date]. Want briefing anyway?"
```

## Meeting Analysis

### High-Priority Meeting Signals

```
EXTERNAL/CLIENT MEETINGS:
- Attendee email domains ≠ company domain
- Title contains client name (match against Notion)
- Location is external address or "Client Site"

PREP-NEEDED SIGNALS:
- No description or agenda
- Large attendee count (>5)
- First meeting with this attendee set
- Title contains "Review", "Presentation", "Demo"
```

### Day Load Assessment

```python
total_meeting_hours = sum(event.duration for event in today_events)

ASSESSMENT:
- Light: <2 hours
- Normal: 2-4 hours  
- Heavy: 4-6 hours    → Note in briefing
- Packed: >6 hours    → Flag as warning

CHECK FOR:
- Back-to-back meetings (no breaks)
- Meetings during lunch (12-1pm)
- Early morning (<8am) or late evening (>6pm)
```

### Conflict Detection

```
CONFLICT TYPES:
1. Hard conflict: Two meetings same time
2. Soft conflict: <15min gap between meetings
3. Travel conflict: In-person meetings too close together

FLAG ALL CONFLICTS IN BRIEFING
```

## Calendar-Based Context

### Working Hours Detection

```
1. Check calendar working hours settings
2. Fallback: Infer from historical meeting patterns
3. Default: 9am-6pm user timezone
```

### Holiday Detection

```
CHECK:
1. Calendar "Holidays" subscribed calendar
2. All-day events with holiday keywords
3. Regional holiday API if available

IF HOLIDAY:
- Previous briefing should include "Next briefing will cover [date range]"
- Post-holiday briefing should span the full gap
```

## Error Handling

```
401 Unauthorized  → Re-authenticate
403 Forbidden     → Calendar not shared, note which
404 Not Found     → Calendar deleted
Timeout           → "Calendar slow, showing cached data"
```
