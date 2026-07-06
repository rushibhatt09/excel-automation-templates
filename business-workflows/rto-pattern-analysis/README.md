# RTO Pattern Analysis - n8n Workflow

**The problem:** RTO (return-to-origin) shipments are pure cost - you pay to ship it out and again to ship
it back, with nothing sold. A few RTOs are normal, but if a specific pincode or SKU keeps coming back, that's
usually a fixable problem (address quality, COD friction, product-market mismatch) hiding in the noise of
overall shipment data.

**What this workflow does:** Compares delivered vs. RTO shipments by pincode and by SKU, flags any pincode
or SKU whose RTO rate crosses a threshold, and breaks down RTO reasons - so you know exactly where to focus.

## Import it

1. Open n8n, go to **Workflows > Import from File**, and select
   [`rto_pattern_analysis_workflow.json`](./rto_pattern_analysis_workflow.json).
2. Click **Execute workflow** - it runs immediately on built-in sample data, no credentials needed.

## Nodes

- **Sample Shipment Outcomes** - 12 sample shipments. Replace with your own courier delivery report - include
  ALL shipments (Delivered and RTO), not just the RTO ones, since the rate calculation needs both. Keep the
  same field names (`awb`, `pincode`, `sku`, `status`, `rtoReason`).
- **Analyze RTO Patterns** - open this node and adjust `RTO_RATE_THRESHOLD` (default 30%) to flag
  pincodes/SKUs worth investigating.
- **Filter: Flagged Pincodes/SKUs** - outputs just the ones over threshold.
- **Summary** - overall RTO rate, top return reasons, and the flagged lists.

## Use cases

- **Courier/3PL conversation starter** - a documented high-RTO pincode pattern is useful evidence when
  asking your courier about delivery-attempt quality in that area.
- **COD policy review** - if "COD Not Ready" dominates the reason breakdown, that's a signal to tighten COD
  confirmation before dispatch.
- **Product-market fit check** - a SKU with a high RTO rate independent of pincode may have a listing,
  sizing, or expectation-mismatch problem worth investigating separately.
