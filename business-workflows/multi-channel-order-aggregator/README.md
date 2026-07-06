# Multi-Channel Order Aggregator - n8n Workflow

**The problem:** Orders come in from your website, and often from one or more marketplaces too - each with
its own export format and dashboard. Getting one clear daily picture means manually copying numbers between
spreadsheets.

**What this workflow does:** Pulls orders from multiple channels, tags each with its source, and combines
them into one unified list with revenue and top-SKU totals - across all channels, in one place.

## Import it

1. Open n8n, go to **Workflows > Import from File**, and select
   [`multi_channel_order_aggregator_workflow.json`](./multi_channel_order_aggregator_workflow.json).
2. Click **Execute workflow** - it runs immediately on built-in sample data, no credentials needed.

## Nodes

- **Website Orders**, **Marketplace A Orders**, **Marketplace B Orders** - one sample source per channel.
  Replace each with your own source (Shopify/WooCommerce node, marketplace API, Google Sheets export, etc.).
  Add or remove channel nodes as needed - just keep the field names consistent (`orderId`, `customerName`,
  `sku`, `qty`, `amount`, `orderDate`) and update **Merge All Channels** to reference any nodes you add/remove.
- **Merge All Channels** - combines all channel outputs into one tagged list. Note: the channel nodes run in
  sequence (not parallel) so this node can reliably reference all of them by name once they've executed.
- **Daily Summary** - total orders, revenue by channel, and top SKUs by units sold across all channels.

## Use cases

- **Daily ops standup** - one number for "how did we do today" instead of checking 3 dashboards.
- **Channel performance comparison** - see which channel is actually driving revenue vs. just order count.
- **Demand planning input** - top-SKU totals feed directly into the Low-Stock Reorder Alert workflow.
