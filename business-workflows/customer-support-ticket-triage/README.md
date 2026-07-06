# Customer Support Ticket Triage - n8n Workflow

**The problem:** Support tickets pile up across email, chat, and social channels, and someone has to read
each one to figure out what it's about and how urgent it is before it can be routed. That's slow and
inconsistent when volume grows.

**What this workflow does:** Reads each ticket's subject and message, categorizes it (Shipping, Product
Issue, Billing, or General), flags urgent language, and routes it to the right team - automatically.

## Import it

1. Open n8n, go to **Workflows > Import from File**, and select
   [`customer_support_ticket_triage_workflow.json`](./customer_support_ticket_triage_workflow.json).
2. Click **Execute workflow** - it runs immediately on built-in sample data, no credentials needed.

## Nodes

- **Sample Support Tickets** - 6 sample tickets. Replace with your own source (helpdesk API, Gmail trigger,
  Google Sheets, etc.). Keep `subject`/`message` fields for keyword matching.
- **Categorize & Prioritize Tickets** - open this node and edit `CATEGORY_RULES` (keyword lists per
  category), `URGENT_KEYWORDS`, and `ROUTE_BY_CATEGORY` (which team each category routes to) to match your
  own vocabulary and team names.
- **Filter: High Priority Only** - outputs tickets needing immediate attention.
- **Summary** - ticket counts by category, priority, and route.

## Use cases

- **First-line triage** - route tickets to the right team before a human ever reads them.
- **Urgent-ticket alerting** - connect a Slack/email node after the High Priority filter for instant alerts.
- **Support volume reporting** - the category/priority breakdown is a ready-made weekly report.

## Note on the keyword approach

This uses simple keyword matching, not an LLM - fast, free, and predictable, but it will miss phrasing it
doesn't recognize. If you want smarter categorization, replace **Categorize & Prioritize Tickets** with an
AI node (OpenAI/Claude) prompted to return the same `category`/`priority`/`route` fields.
