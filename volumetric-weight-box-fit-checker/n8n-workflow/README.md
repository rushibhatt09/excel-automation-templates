# Volumetric Weight & Box-Fit Checker - n8n Workflow

The same fit-check logic as `Volumetric_Weight_Box_Fit_Checker.xlsx`, as an importable n8n workflow.

## Import it

1. Open n8n, go to **Workflows > Import from File**, and select
   [`box_fit_checker_workflow.json`](./box_fit_checker_workflow.json).
2. Click **Execute workflow** - it runs immediately on built-in sample data, no credentials needed.

## Nodes

- **Box Library** - your carton sizes, ordered smallest/cheapest to largest/costliest. Edit the
  `BOX_LIBRARY` array with your own packaging.
- **Sample Product Data** - the 10 sample products (same ones as the Excel template). Replace with a real
  source: Google Sheets, HTTP Request, or Read Binary File + Extract from File for an uploaded .xlsx/.csv.
  Keep the same field names (`sku`, `name`, `length`, `width`, `height`, `weight`) and enter Length = longest
  side, Width = middle side, Height = shortest side.
- **Fit Checker** - matches each product to the cheapest box that fits, or flags "NO BOX FITS".
- **Filter: Needs Review** - outputs products with no fitting box.
- **Summary** - outputs the same totals as the Excel Summary tab (total packaging cost, box usage
  breakdown, etc).

Verified to produce identical results to the Excel template on the same sample data: 10 products checked, 1
flagged for review, ₹111 total recommended packaging cost.

## Next step: auto-draft the packaging review notice

[`packaging_review_notice_workflow.json`](./packaging_review_notice_workflow.json) takes the "Filter: Needs
Review" output above and drafts an internal notice for your packaging/procurement team - one per product,
plus one consolidated notice. Unlike the two audit workflows, this isn't a vendor dispute (there's no vendor
overcharging you for a packaging-fit issue) - it's an internal alert. It only drafts; connect a
Slack/Email/Teams node to actually send. Import it the same way as above.
