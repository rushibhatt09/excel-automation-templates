# Low-Stock Reorder Alert - n8n Workflow

**The problem:** Reordering too late means stockouts and lost sales; reordering too early ties up cash in
inventory you don't need yet. Most small teams just eyeball stock levels, which doesn't scale past a
handful of SKUs.

**What this workflow does:** Compares current stock to a reorder point calculated from your average daily
sales, supplier lead time, and a safety buffer - then tells you exactly which SKUs need reordering and how
many units to order.

## Import it

1. Open n8n, go to **Workflows > Import from File**, and select
   [`low_stock_reorder_alert_workflow.json`](./low_stock_reorder_alert_workflow.json).
2. Click **Execute workflow** - it runs immediately on built-in sample data, no credentials needed.

## Nodes

- **Sample Inventory Data** - 6 sample SKUs. Replace with your own source (Google Sheets, HTTP Request,
  database query, etc.). Keep the same field names (`sku`, `name`, `currentStock`, `avgDailySales`,
  `leadTimeDays`, `safetyBufferDays`, `supplier`).
- **Calculate Reorder Points** - the math: reorder point = (avg daily sales x lead time days) + safety stock
  (avg daily sales x safety buffer days). Suggested reorder quantity brings stock up to 1.5x the reorder
  point.
- **Filter: Needs Reorder** - outputs just the SKUs at or below their reorder point.
- **Summary** - total units to reorder, broken down by supplier (handy for splitting purchase orders).

## Use cases

- **Weekly/monthly reorder planning** - run this against your latest stock export to get a ready reorder list.
- **Purchase order splitting** - the supplier breakdown tells you exactly what to order from whom.
- **New SKU launch planning** - plug in projected daily sales before a launch to estimate initial reorder needs.
