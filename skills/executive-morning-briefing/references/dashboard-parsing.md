# Dashboard Parsing Reference

## Connection Setup

Dashboards are the most variable integration—there's no universal connector.

### For Claude.ai Users
Most dashboards require one of:
- **Screenshot sharing**: User shares image, skill uses vision to extract metrics
- **Manual reporting**: User tells you the numbers: "MRR is $847K"
- **URL with embedded auth**: Some dashboards (Notion embeds, public Looker) work via URL

Prompt once: "What's your key dashboard? You can share a screenshot, give me a link, or just tell me the numbers."

### For Developers
Implement based on your dashboard stack:
- ChartMogul/Stripe: Use their APIs with OAuth
- Google Sheets dashboard: Use Sheets API
- Custom BI tool: Build authenticated fetch
- No API: Default to screenshot or manual mode

## Data Input Modes

### Mode 1: Direct API/URL Access
When you have authenticated access to dashboard URLs or APIs.

### Mode 2: Screenshot (Vision)
When user shares a dashboard screenshot. Use vision to:
- Read metric names and values
- Identify color coding (red/yellow/green)
- Detect trend arrows and sparklines
- Note any text that's unclear

If something is illegible: "I can see the MRR chart but can't read the exact number—what is it?"

### Mode 3: User-Provided Numbers
When user pastes or dictates metrics. Accept any format:
- "MRR is 847K, down from 860K"
- "Pipeline: $2.1M (was $2.4M)"
- "MQLs this month: 342, target was 400"

Parse naturally. Don't require structured input.

### Mode 4: No Dashboard Access
When no dashboard data is available, ask once:
"What are your key numbers this morning? MRR, pipeline, conversion—whatever you track."

If user doesn't know or doesn't want to share, skip dashboard section entirely. Don't nag.

## Supported Formats (API Mode)

| Format | Parsing Approach |
|--------|------------------|
| Web (HTML) | DOM parsing, table extraction |
| Google Sheets | Sheets API, cell conditional formatting |
| Excel (.xlsx) | OpenPyXL parsing, conditional formatting |
| PDF | Text extraction, visual indicators |
| PowerPoint | Slide text extraction |
| Google Slides | Slides API |
| Looker/Metabase | Embed URL as HTML |
| Custom Dashboards | HTML parsing with heuristics |

## OAuth Handling

Authentication flow:
1. Attempt URL fetch
2. If 401/403, check if OAuth flow available:
   - Google property: Use Google OAuth token
   - Microsoft property: Use M365 OAuth token
   - Custom auth: Note "requires manual authentication"
3. If OAuth available, use token
4. If still fails, use graceful degradation message

Graceful failure: "Dashboard at [URL] requires manual check—authentication failed."

## Alert State Detection

### Color-Based Detection

**Red indicators:**
- CSS: color containing "red", "danger", "error"
- CSS: background-color in red spectrum (#ff0000 - #cc0000)
- Class names: "danger", "critical", "alert", "error", "red"
- Cell fill: Red family in Excel/Sheets

**Yellow/Amber indicators:**
- CSS: "warning", "amber", "yellow", "caution"
- Class names: "warning", "caution", "yellow"
- Cell fill: Yellow/orange family

**Green indicators (for completeness):**
- CSS: "success", "good", "green"
- Class names: "success", "ok", "green"

### Text-Based Detection

```python
ALERT_KEYWORDS = {
    "critical": "RED",
    "alert": "RED", 
    "danger": "RED",
    "failed": "RED",
    "error": "RED",
    "down": "RED",
    "below target": "RED",
    "at risk": "RED",
    
    "warning": "YELLOW",
    "caution": "YELLOW",
    "declining": "YELLOW",
    "trending down": "YELLOW",
    "needs attention": "YELLOW",
    "monitor": "YELLOW"
}
```

### Trend Detection

**Trend signals:**
- Arrows: ↓ ↑ → ▼ ▲ (Unicode)
- Icons: down-arrow, up-arrow classes
- Text: "down X%", "up X%", "-X%", "+X%"
- Sparklines: Visual trend direction

**Negative trend thresholds:**
- Down >10% from previous period: Flag
- Down >5% for 3+ consecutive periods: Flag
- Below target/threshold: Flag

## Format-Specific Parsing

### HTML Dashboards

Extraction strategy:
1. Find all `<table>` elements
2. Find KPI cards (div with metric + label pattern)
3. Find charts (common charting libraries: Highcharts, Chart.js, D3)
4. Extract text + associated styling

Table parsing extracts: header row (column names), data rows (values + cell styling), conditional formatting classes, and outputs metric, value, trend, status.

### Google Sheets

API approach:
```
GET /spreadsheets/{id}?includeGridData=true
```

Extract: cell values, cell backgroundColor (for conditional formatting), cell textFormat (bold = important), named ranges (often indicate key metrics).

Conditional formatting: Fetch via `spreadsheets.get` with `fields=sheets.conditionalFormats`. Map rules to cells to understand what triggers red/yellow.

### Excel Files

```python
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

wb = load_workbook(file, data_only=True)
for sheet in wb.worksheets:
    for row in sheet.iter_rows():
        for cell in row:
            fill = cell.fill
            if fill.fgColor.rgb in RED_COLORS:
                # This is an alert cell
```

### PDF Dashboards

Text extraction approach:
- Use pdfplumber or PyMuPDF
- Look for table structures
- Search for alert keywords
- Note: Visual indicators may be lost

Strategy:
1. Extract all text
2. Look for metric patterns: "Metric: Value"
3. Search for alert keywords near values
4. Note limitations: "PDF dashboard—some visual alerts may not be captured"

## Metric Extraction

```
OUTPUT STRUCTURE FOR EACH METRIC:
{
  "name": "Monthly Recurring Revenue",
  "value": "$125,000",
  "trend": "down 8%",
  "status": "YELLOW",
  "threshold": "$135,000",  // if available
  "detail_link": "https://..."  // if available
}

INCLUDE IN BRIEFING:
- Only RED and YELLOW status metrics
- GREEN metrics only if user explicitly asks
```

## Error Handling

| Error | Response |
|-------|----------|
| 401/403 | "Dashboard requires authentication" |
| 404 | "Dashboard URL not found—verify link" |
| Timeout | "Dashboard slow to load—check manually" |
| Parse error | "Couldn't parse dashboard format" |
| No data | "Dashboard loaded but no metrics found" |
| Screenshot illegible | "Can't read [specific part]—what's the number?" |

ALWAYS: Continue briefing with other sources.
NEVER: Fail entire briefing due to dashboard issues.
```
