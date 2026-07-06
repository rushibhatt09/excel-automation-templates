import sys
sys.path.insert(0, r"C:\Users\micro\OneDrive\Documents\excel-automation-templates\scripts")
from n8n_helpers import node, code_node, sticky, chain, branch, merge_connections, workflow, save_workflow

BASE = r"C:\Users\micro\OneDrive\Documents\excel-automation-templates"

# ============================================================
# 1. Low-Stock Reorder Alert
# ============================================================

trigger1 = node("When clicking \"Execute workflow\"", "n8n-nodes-base.manualTrigger", {}, [-200, 300])

sample_inventory = code_node("Sample Inventory Data", r'''
// Replace this node with your own source (Google Sheets, HTTP Request, database, etc.)
const inventory = [
  { sku: "SKU-2001", name: "Vitamin C Serum 30ml", currentStock: 40, avgDailySales: 8, leadTimeDays: 7, safetyBufferDays: 3, supplier: "Supplier A" },
  { sku: "SKU-2002", name: "Sunscreen SPF50", currentStock: 120, avgDailySales: 10, leadTimeDays: 10, safetyBufferDays: 4, supplier: "Supplier B" },
  { sku: "SKU-2003", name: "Face Wash 100ml", currentStock: 15, avgDailySales: 6, leadTimeDays: 5, safetyBufferDays: 2, supplier: "Supplier A" },
  { sku: "SKU-2004", name: "Night Repair Cream", currentStock: 60, avgDailySales: 3, leadTimeDays: 14, safetyBufferDays: 5, supplier: "Supplier C" },
  { sku: "SKU-2005", name: "Lip Balm Combo", currentStock: 8, avgDailySales: 4, leadTimeDays: 6, safetyBufferDays: 3, supplier: "Supplier B" },
  { sku: "SKU-2006", name: "Hair Serum 50ml", currentStock: 200, avgDailySales: 5, leadTimeDays: 12, safetyBufferDays: 4, supplier: "Supplier C" },
];
return inventory.map(i => ({ json: i }));
'''.strip(), [40, 300])

calc_reorder = code_node("Calculate Reorder Points", r'''
return $input.all().map(item => {
  const s = item.json;
  const safetyStock = s.avgDailySales * s.safetyBufferDays;
  const reorderPoint = Math.ceil(s.avgDailySales * s.leadTimeDays + safetyStock);
  const needsReorder = s.currentStock <= reorderPoint;
  const targetStock = Math.ceil(reorderPoint * 1.5);
  const suggestedReorderQty = needsReorder ? Math.max(0, targetStock - s.currentStock) : 0;
  return { json: { ...s, safetyStock, reorderPoint, needsReorder, suggestedReorderQty } };
});
'''.strip(), [280, 300])

filter1 = code_node("Filter: Needs Reorder", 'return $input.all().filter(item => item.json.needsReorder);', [560, 160])

summary1 = code_node("Summary", r'''
const items = $input.all().map(i => i.json);
const needsReorder = items.filter(i => i.needsReorder);
const totalUnitsToReorder = needsReorder.reduce((s,i)=>s+i.suggestedReorderQty, 0);
const suppliers = [...new Set(items.map(i => i.supplier))];
const supplierBreakdown = suppliers.map(sup => {
  const si = needsReorder.filter(i => i.supplier === sup);
  return { supplier: sup, skusToReorder: si.length, unitsToReorder: si.reduce((s,i)=>s+i.suggestedReorderQty,0) };
});
return [{ json: {
  totalSkusChecked: items.length,
  skusNeedingReorder: needsReorder.length,
  totalUnitsToReorder,
  supplierBreakdown,
}}];
'''.strip(), [560, 440])

note1 = sticky(
    "## Low-Stock Reorder Alert\n\n"
    "Compares current stock to a reorder point (lead time + safety buffer, based on average daily sales) "
    "and suggests how much to reorder.\n\n"
    "1. Replace **Sample Inventory Data** with your own source (Google Sheets, HTTP Request, database "
    "query, etc.) - keep the same field names.\n"
    "2. **Calculate Reorder Points** does the math - reorder point = avg daily sales x (lead time + safety "
    "buffer days).\n"
    "3. **Filter: Needs Reorder** outputs just the SKUs below their reorder point.\n"
    "4. **Summary** gives total units to reorder, broken down by supplier - handy for splitting purchase "
    "orders.\n"
    "5. Connect a Slack/Email node after Filter or Summary to get alerted automatically.",
    [-200, -60], width=780, height=240,
)

nodes1 = [trigger1, sample_inventory, calc_reorder, filter1, summary1, note1]
connections1 = merge_connections(
    chain("When clicking \"Execute workflow\"", "Sample Inventory Data", "Calculate Reorder Points"),
    branch("Calculate Reorder Points", ["Filter: Needs Reorder", "Summary"]),
)
wf1 = workflow("Low-Stock Reorder Alert", nodes1, connections1)
save_workflow(wf1, rf"{BASE}\business-workflows\low-stock-reorder-alert\low_stock_reorder_alert_workflow.json")
print("saved business workflow 1")


# ============================================================
# 2. Multi-Channel Order Aggregator
# ============================================================

trigger2 = node("When clicking \"Execute workflow\"", "n8n-nodes-base.manualTrigger", {}, [-200, 300])

website_orders = code_node("Website Orders", r'''
// Replace with your own source (Shopify/WooCommerce node, Google Sheets, HTTP Request, etc.)
const orders = [
  { orderId: "WEB-1001", customerName: "A. Sharma", sku: "SKU-2001", qty: 2, amount: 1798, orderDate: "2026-07-01" },
  { orderId: "WEB-1002", customerName: "R. Iyer", sku: "SKU-2003", qty: 1, amount: 399, orderDate: "2026-07-01" },
  { orderId: "WEB-1003", customerName: "P. Nair", sku: "SKU-2005", qty: 3, amount: 897, orderDate: "2026-07-02" },
];
return orders.map(o => ({ json: { ...o, channel: "Website" } }));
'''.strip(), [40, 160])

marketplace_a_orders = code_node("Marketplace A Orders", r'''
// Replace with your own source for this marketplace's order export/API
const orders = [
  { orderId: "MPA-5001", customerName: "S. Verma", sku: "SKU-2002", qty: 1, amount: 899, orderDate: "2026-07-01" },
  { orderId: "MPA-5002", customerName: "K. Das", sku: "SKU-2001", qty: 1, amount: 899, orderDate: "2026-07-02" },
];
return orders.map(o => ({ json: { ...o, channel: "Marketplace A" } }));
'''.strip(), [40, 300])

marketplace_b_orders = code_node("Marketplace B Orders", r'''
// Replace with your own source for this marketplace's order export/API
const orders = [
  { orderId: "MPB-9001", customerName: "T. Menon", sku: "SKU-2004", qty: 1, amount: 1299, orderDate: "2026-07-01" },
  { orderId: "MPB-9002", customerName: "N. Rao", sku: "SKU-2006", qty: 2, amount: 1798, orderDate: "2026-07-02" },
  { orderId: "MPB-9003", customerName: "V. Pillai", sku: "SKU-2002", qty: 1, amount: 899, orderDate: "2026-07-02" },
];
return orders.map(o => ({ json: { ...o, channel: "Marketplace B" } }));
'''.strip(), [40, 440])

merge_channels = code_node("Merge All Channels", r'''
const website = $("Website Orders").all().map(i => i.json);
const mpA = $("Marketplace A Orders").all().map(i => i.json);
const mpB = $("Marketplace B Orders").all().map(i => i.json);
return [...website, ...mpA, ...mpB].map(o => ({ json: o }));
'''.strip(), [340, 300])

daily_summary = code_node("Daily Summary", r'''
const items = $input.all().map(i => i.json);
const totalOrders = items.length;
const totalRevenue = items.reduce((s,i)=>s+i.amount, 0);
const channels = [...new Set(items.map(i => i.channel))];
const channelBreakdown = channels.map(c => {
  const ci = items.filter(i => i.channel === c);
  return { channel: c, orders: ci.length, revenue: ci.reduce((s,i)=>s+i.amount,0) };
});
const unitsBySku = {};
items.forEach(i => { unitsBySku[i.sku] = (unitsBySku[i.sku] || 0) + i.qty; });
const topSkus = Object.entries(unitsBySku).sort((a,b)=>b[1]-a[1]).map(([sku, units]) => ({ sku, units }));
return [{ json: { totalOrders, totalRevenue, channelBreakdown, topSkusByUnits: topSkus } }];
'''.strip(), [620, 300])

note2 = sticky(
    "## Multi-Channel Order Aggregator\n\n"
    "Combines orders from multiple sales channels into one unified daily log with totals.\n\n"
    "1. Replace **Website Orders**, **Marketplace A Orders**, **Marketplace B Orders** with your own "
    "sources (Shopify/WooCommerce nodes, marketplace APIs, Google Sheets, etc.) - add or remove channel "
    "nodes as needed, just update the names referenced in **Merge All Channels**.\n"
    "2. **Merge All Channels** combines everything into one list, tagged by channel.\n"
    "3. **Daily Summary** gives total orders, revenue by channel, and top SKUs by units sold.\n\n"
    "Note: all three channel nodes run in sequence (not parallel) so **Merge All Channels** can reliably "
    "reference all of them by name once they've all executed.",
    [-200, -80], width=780, height=260,
)

nodes2 = [trigger2, website_orders, marketplace_a_orders, marketplace_b_orders, merge_channels, daily_summary, note2]
connections2 = chain(
    "When clicking \"Execute workflow\"", "Website Orders", "Marketplace A Orders", "Marketplace B Orders",
    "Merge All Channels", "Daily Summary",
)
wf2 = workflow("Multi-Channel Order Aggregator", nodes2, connections2)
save_workflow(wf2, rf"{BASE}\business-workflows\multi-channel-order-aggregator\multi_channel_order_aggregator_workflow.json")
print("saved business workflow 2")


# ============================================================
# 3. Customer Support Ticket Triage
# ============================================================

trigger3 = node("When clicking \"Execute workflow\"", "n8n-nodes-base.manualTrigger", {}, [-200, 300])

sample_tickets = code_node("Sample Support Tickets", r'''
// Replace this node with your own source (helpdesk API, Gmail trigger, Google Sheets, etc.)
const tickets = [
  { ticketId: "T-1001", customerName: "A. Sharma", channel: "Email", subject: "Where is my order?", message: "It has been 6 days and my order is still not delivered, please help." },
  { ticketId: "T-1002", customerName: "R. Iyer", channel: "Chat", subject: "Product arrived broken", message: "The bottle was damaged and leaking when it arrived, this is unacceptable." },
  { ticketId: "T-1003", customerName: "P. Nair", channel: "Email", subject: "Refund request", message: "I want to cancel my order and get a refund immediately, this is urgent." },
  { ticketId: "T-1004", customerName: "S. Verma", channel: "Instagram", subject: "Question about ingredients", message: "Does this serum contain any fragrance?" },
  { ticketId: "T-1005", customerName: "K. Das", channel: "Chat", subject: "Tracking not updating", message: "My tracking link has not moved in 3 days, is my package lost?" },
  { ticketId: "T-1006", customerName: "T. Menon", channel: "Email", subject: "Wrong item received", message: "I ordered the day cream but received the night cream instead." },
];
return tickets.map(t => ({ json: t }));
'''.strip(), [40, 300])

categorize_tickets = code_node("Categorize & Prioritize Tickets", r'''
// EDIT THIS: keyword rules for category and urgency detection
const CATEGORY_RULES = [
  { category: "Shipping", keywords: ["where is my order", "tracking", "delivery", "delivered", "shipped", "lost"] },
  { category: "Product Issue", keywords: ["broken", "damaged", "defective", "leaking", "wrong item"] },
  { category: "Billing", keywords: ["refund", "cancel", "charged", "payment", "invoice"] },
];
const URGENT_KEYWORDS = ["urgent", "immediately", "asap", "unacceptable", "angry", "still not"];

function detectCategory(text) {
  for (const rule of CATEGORY_RULES) {
    if (rule.keywords.some(k => text.includes(k))) return rule.category;
  }
  return "General";
}
function isUrgent(text) {
  return URGENT_KEYWORDS.some(k => text.includes(k));
}

const ROUTE_BY_CATEGORY = {
  "Shipping": "Logistics Team",
  "Product Issue": "Quality/Returns Team",
  "Billing": "Finance Team",
  "General": "General Support Queue",
};

return $input.all().map(item => {
  const t = item.json;
  const text = `${t.subject} ${t.message}`.toLowerCase();
  const category = detectCategory(text);
  const urgent = isUrgent(text);
  const priority = urgent ? "High" : (category === "General" ? "Low" : "Medium");
  const route = ROUTE_BY_CATEGORY[category];
  return { json: { ...t, category, priority, route } };
});
'''.strip(), [280, 300])

filter3 = code_node("Filter: High Priority Only", 'return $input.all().filter(item => item.json.priority === "High");', [560, 160])

summary3 = code_node("Summary", r'''
const items = $input.all().map(i => i.json);
const categories = [...new Set(items.map(i => i.category))];
const categoryBreakdown = categories.map(c => ({ category: c, tickets: items.filter(i => i.category === c).length }));
const priorities = ["High", "Medium", "Low"];
const priorityBreakdown = priorities.map(p => ({ priority: p, tickets: items.filter(i => i.priority === p).length }));
const routes = [...new Set(items.map(i => i.route))];
const routeBreakdown = routes.map(r => ({ route: r, tickets: items.filter(i => i.route === r).length }));
return [{ json: { totalTickets: items.length, categoryBreakdown, priorityBreakdown, routeBreakdown } }];
'''.strip(), [560, 440])

note3 = sticky(
    "## Customer Support Ticket Triage\n\n"
    "Categorizes incoming tickets by keyword, assigns a priority, and routes each to the right team.\n\n"
    "1. Replace **Sample Support Tickets** with your own source (helpdesk API, Gmail trigger, Google "
    "Sheets, etc.) - keep `subject`/`message` fields for keyword matching.\n"
    "2. Open **Categorize & Prioritize Tickets** and edit `CATEGORY_RULES`, `URGENT_KEYWORDS`, and "
    "`ROUTE_BY_CATEGORY` to match your own categories and team names.\n"
    "3. **Filter: High Priority Only** outputs tickets needing immediate attention.\n"
    "4. **Summary** gives ticket counts by category, priority, and route.",
    [-200, -60], width=780, height=220,
)

nodes3 = [trigger3, sample_tickets, categorize_tickets, filter3, summary3, note3]
connections3 = merge_connections(
    chain("When clicking \"Execute workflow\"", "Sample Support Tickets", "Categorize & Prioritize Tickets"),
    branch("Categorize & Prioritize Tickets", ["Filter: High Priority Only", "Summary"]),
)
wf3 = workflow("Customer Support Ticket Triage", nodes3, connections3)
save_workflow(wf3, rf"{BASE}\business-workflows\customer-support-ticket-triage\customer_support_ticket_triage_workflow.json")
print("saved business workflow 3")


# ============================================================
# 4. RTO Pattern Analysis
# ============================================================

trigger4 = node("When clicking \"Execute workflow\"", "n8n-nodes-base.manualTrigger", {}, [-200, 300])

sample_shipment_outcomes = code_node("Sample Shipment Outcomes", r'''
// Replace this node with your own source (courier delivery report, Google Sheets, HTTP Request, etc.)
// Include ALL shipments (Delivered and RTO), not just the RTO ones - the rate calculation needs both.
const shipments = [
  { awb: "AWB3001", pincode: "560001", sku: "SKU-2001", status: "Delivered" },
  { awb: "AWB3002", pincode: "560001", sku: "SKU-2002", status: "Delivered" },
  { awb: "AWB3003", pincode: "560001", sku: "SKU-2001", status: "RTO", rtoReason: "Customer Refused" },
  { awb: "AWB3004", pincode: "560002", sku: "SKU-2003", status: "Delivered" },
  { awb: "AWB3005", pincode: "560002", sku: "SKU-2003", status: "RTO", rtoReason: "Address Not Found" },
  { awb: "AWB3006", pincode: "560002", sku: "SKU-2004", status: "RTO", rtoReason: "Address Not Found" },
  { awb: "AWB3007", pincode: "560002", sku: "SKU-2001", status: "RTO", rtoReason: "Customer Refused" },
  { awb: "AWB3008", pincode: "560003", sku: "SKU-2005", status: "Delivered" },
  { awb: "AWB3009", pincode: "560003", sku: "SKU-2005", status: "Delivered" },
  { awb: "AWB3010", pincode: "560003", sku: "SKU-2006", status: "Delivered" },
  { awb: "AWB3011", pincode: "560001", sku: "SKU-2002", status: "RTO", rtoReason: "COD Not Ready" },
  { awb: "AWB3012", pincode: "560002", sku: "SKU-2004", status: "Delivered" },
];
return shipments.map(s => ({ json: s }));
'''.strip(), [40, 300])

analyze_rto = code_node("Analyze RTO Patterns", r'''
// EDIT THIS: RTO rate above which a pincode/SKU gets flagged for review
const RTO_RATE_THRESHOLD = 0.30;

const items = $input.all().map(i => i.json);

function groupRate(key) {
  const groups = {};
  items.forEach(s => {
    groups[s[key]] = groups[s[key]] || { total: 0, rto: 0 };
    groups[s[key]].total += 1;
    if (s.status === "RTO") groups[s[key]].rto += 1;
  });
  return Object.entries(groups).map(([value, g]) => ({
    [key]: value,
    totalShipments: g.total,
    rtoShipments: g.rto,
    rtoRate: Math.round((g.rto / g.total) * 1000) / 1000,
    flagged: (g.rto / g.total) >= RTO_RATE_THRESHOLD,
  }));
}

const pincodeBreakdown = groupRate("pincode");
const skuBreakdown = groupRate("sku");

const reasonCounts = {};
items.filter(s => s.status === "RTO").forEach(s => {
  reasonCounts[s.rtoReason] = (reasonCounts[s.rtoReason] || 0) + 1;
});
const reasonBreakdown = Object.entries(reasonCounts).map(([reason, count]) => ({ reason, count }));

return [{ json: { pincodeBreakdown, skuBreakdown, reasonBreakdown } }];
'''.strip(), [280, 300])

filter4 = code_node("Filter: Flagged Pincodes/SKUs", r'''
const data = $input.first().json;
const flaggedPincodes = data.pincodeBreakdown.filter(p => p.flagged);
const flaggedSkus = data.skuBreakdown.filter(s => s.flagged);
return [{ json: { flaggedPincodes, flaggedSkus } }];
'''.strip(), [560, 160])

summary4 = code_node("Summary", r'''
const outcomes = $("Sample Shipment Outcomes").all().map(i => i.json);
const analysis = $("Analyze RTO Patterns").first().json;
const totalShipments = outcomes.length;
const totalRto = outcomes.filter(s => s.status === "RTO").length;
const overallRtoRate = Math.round((totalRto / totalShipments) * 1000) / 1000;
return [{ json: {
  totalShipments,
  totalRto,
  overallRtoRate,
  topRtoReasons: analysis.reasonBreakdown.sort((a,b)=>b.count-a.count),
  flaggedPincodes: analysis.pincodeBreakdown.filter(p => p.flagged),
  flaggedSkus: analysis.skuBreakdown.filter(s => s.flagged),
}}];
'''.strip(), [560, 440])

note4 = sticky(
    "## RTO Pattern Analysis\n\n"
    "Analyzes delivered vs. returned-to-origin (RTO) shipments to flag pincodes and SKUs with an "
    "unusually high RTO rate, and breaks down RTO reasons.\n\n"
    "1. Replace **Sample Shipment Outcomes** with your own courier delivery report - include ALL "
    "shipments (Delivered and RTO), not just the RTO ones, since the rate needs both.\n"
    "2. Open **Analyze RTO Patterns** and adjust `RTO_RATE_THRESHOLD` (default 30%) to flag pincodes/SKUs "
    "worth investigating.\n"
    "3. **Filter: Flagged Pincodes/SKUs** outputs just the ones over threshold.\n"
    "4. **Summary** gives the overall RTO rate, top return reasons, and the flagged lists.",
    [-200, -60], width=780, height=240,
)

nodes4 = [trigger4, sample_shipment_outcomes, analyze_rto, filter4, summary4, note4]
connections4 = merge_connections(
    chain("When clicking \"Execute workflow\"", "Sample Shipment Outcomes", "Analyze RTO Patterns"),
    branch("Analyze RTO Patterns", ["Filter: Flagged Pincodes/SKUs", "Summary"]),
)
wf4 = workflow("RTO Pattern Analysis", nodes4, connections4)
save_workflow(wf4, rf"{BASE}\business-workflows\rto-pattern-analysis\rto_pattern_analysis_workflow.json")
print("saved business workflow 4")
