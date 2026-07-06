# Business Automation Workflows

Standalone n8n workflows for common ops/admin tasks beyond billing audits - no coding, no credentials
required to try them (each ships with built-in sample data you can run immediately).

| Workflow | What it solves |
|---|---|
| [Low-Stock Reorder Alert](./low-stock-reorder-alert) | Flags SKUs below their reorder point and suggests how much to order |
| [Multi-Channel Order Aggregator](./multi-channel-order-aggregator) | Combines orders from multiple sales channels into one daily log with totals |
| [Customer Support Ticket Triage](./customer-support-ticket-triage) | Categorizes and routes support tickets by keyword and urgency |
| [RTO Pattern Analysis](./rto-pattern-analysis) | Flags pincodes/SKUs with unusually high return-to-origin rates |

## How to use any workflow here

1. Open n8n, go to **Workflows > Import from File**, and select the `.json` file in the workflow's folder.
2. Click **Execute workflow** - it runs immediately on the built-in sample data.
3. Open the first Code node (usually named "Sample ...") and replace it with your own data source (Google
   Sheets, HTTP Request, a trigger node, etc.) - keep the same field names.
4. Any node with an `// EDIT THIS` comment at the top has the settings you're meant to customize (thresholds,
   category rules, routing).

## Relationship to the audit templates

These are separate from (not required by) the [Courier Billing Audit](../courier-billing-audit),
[Payment Gateway TDR Audit](../payment-gateway-tdr-audit), and
[Volumetric Weight & Box-Fit Checker](../volumetric-weight-box-fit-checker) templates - they cover different
parts of day-to-day ops. Each of those three templates also has its own n8n workflow and a "next step"
extension workflow (e.g. auto-drafting a dispute email) in its own `n8n-workflow/` folder.
