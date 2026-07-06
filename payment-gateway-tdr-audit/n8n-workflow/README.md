# Payment Gateway TDR Audit - n8n Workflow

The same audit logic as `Payment_Gateway_TDR_Audit_Template.xlsx`, as an importable n8n workflow.

## Import it

1. Open n8n, go to **Workflows > Import from File**, and select
   [`payment_gateway_tdr_audit_workflow.json`](./payment_gateway_tdr_audit_workflow.json).
2. Click **Execute workflow** - it runs immediately on built-in sample data, no credentials needed.

## Nodes

- **Sample Settlement Data** - the 12 sample transactions (same ones as the Excel template). Replace with a
  real source: Google Sheets, HTTP Request, or Read Binary File + Extract from File for an uploaded
  .xlsx/.csv. Keep the same field names (`transactionId`, `paymentMethod`, `transactionAmount`,
  `actualTdrDeducted`, `actualGstDeducted`).
- **Audit Transactions** - open this node and edit the `RATE_CARD` object at the top with your own gateway's
  contracted TDR and GST rates. This is the only place you need to change numbers.
- **Filter: Overcharged Only** - outputs just the disputed transactions.
- **Summary Dashboard** - outputs the same totals as the Excel Summary Dashboard tab (total overcharge,
  payment-method breakdown, etc).

Verified to produce identical results to the Excel template on the same sample data: 9 of 12 transactions
overcharged, ₹293 refund claimable.
