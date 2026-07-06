# Courier Billing Audit - n8n Workflow

The same audit logic as `Courier_Billing_Audit_Template.xlsx`, as an importable n8n workflow.

## Import it

1. Open n8n, go to **Workflows > Import from File**, and select
   [`courier_billing_audit_workflow.json`](./courier_billing_audit_workflow.json).
2. Click **Execute workflow** - it runs immediately on built-in sample data, no credentials needed.

## Nodes

- **Sample Shipment Data** - the 12 sample shipments (same ones as the Excel template). Replace with a real
  source: Google Sheets, HTTP Request, or Read Binary File + Extract from File for an uploaded .xlsx/.csv.
  Keep the same field names (`awb`, `zone`, `paymentMode`, `orderValue`, `actualWeight`, `length`, `width`,
  `height`, `status`, `billedWeight`, `billedAmount`).
- **Audit Shipments** - open this node and edit the `RATE_CARD` object at the top with your own courier's
  contracted zone rates. This is the only place you need to change numbers.
- **Filter: Overcharged Only** - outputs just the disputed shipments.
- **Summary Dashboard** - outputs the same totals as the Excel Summary Dashboard tab (total overcharge,
  zone-wise breakdown, etc).

Verified to produce identical results to the Excel template on the same sample data: 9 of 12 shipments
overcharged, ₹323 refund claimable.
