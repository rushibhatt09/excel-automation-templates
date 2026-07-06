import json
import uuid

BASE = r"C:\Users\micro\OneDrive\Documents\excel-automation-templates"


def node(name, ntype, params, position, type_version=1):
    return {
        "parameters": params,
        "id": str(uuid.uuid4()),
        "name": name,
        "type": ntype,
        "typeVersion": type_version,
        "position": position,
    }


def code_node(name, js_code, position):
    return node(name, "n8n-nodes-base.code", {"jsCode": js_code}, position, type_version=2)


def sticky(content, position, width=340, height=260, color=None):
    params = {"content": content, "height": height, "width": width}
    if color is not None:
        params["color"] = color
    return node("Sticky Note", "n8n-nodes-base.stickyNote", params, position, type_version=1)


def chain(*names):
    """Build a simple linear connections dict: names[0] -> names[1] -> ... """
    conn = {}
    for a, b in zip(names, names[1:]):
        conn.setdefault(a, {"main": [[]]})
        conn[a]["main"][0].append({"node": b, "type": "main", "index": 0})
    return conn


def branch(source, targets):
    return {source: {"main": [[{"node": t, "type": "main", "index": 0} for t in targets]]}}


def merge_connections(*dicts):
    out = {}
    for d in dicts:
        for k, v in d.items():
            if k not in out:
                out[k] = v
            else:
                out[k]["main"][0].extend(v["main"][0])
    return out


def workflow(name, nodes, connections):
    return {
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "pinData": {},
        "settings": {"executionOrder": "v1"},
    }


# ============================================================
# 1. Courier Billing Audit
# ============================================================

trigger1 = node("When clicking \"Execute workflow\"", "n8n-nodes-base.manualTrigger", {}, [-200, 300])

sample_data_code = r'''
// Replace this node with your own data source (Google Sheets, HTTP Request, Read Binary File, etc.)
// Each item below matches one row of the "Shipment Data" tab in the Excel template.
const sampleShipments = [
  ["AWB1001","ORD5001","A","Prepaid",899,0.4,20,15,10,"Delivered",1.0,75],
  ["AWB1002","ORD5002","B","COD",1499,0.8,25,20,12,"Delivered",1.5,115],
  ["AWB1003","ORD5003","C","Prepaid",2199,1.2,30,25,15,"Delivered",2.5,173],
  ["AWB1004","ORD5004","D","COD",999,0.3,15,15,10,"RTO",0.5,200],
  ["AWB1005","ORD5005","E","Prepaid",3499,2.1,40,30,20,"Delivered",5.0,560],
  ["AWB1006","ORD5006","A","COD",599,0.2,12,10,8,"Delivered",0.5,65],
  ["AWB1007","ORD5007","B","Prepaid",1299,0.6,22,18,10,"Delivered",1.0,80],
  ["AWB1008","ORD5008","C","COD",1799,1.0,28,22,14,"RTO",2.0,341],
  ["AWB1009","ORD5009","D","Prepaid",2599,1.8,35,28,18,"Delivered",4.0,305],
  ["AWB1010","ORD5010","E","COD",4299,3.0,45,35,25,"Delivered",8.0,926],
  ["AWB1011","ORD5011","A","Prepaid",749,0.35,18,14,9,"Delivered",0.5,55],
  ["AWB1012","ORD5012","B","Prepaid",1099,0.5,20,16,11,"Delivered",1.0,45],
];
const cols = ["awb","orderId","zone","paymentMode","orderValue","actualWeight","length","width","height","status","billedWeight","billedAmount"];
return sampleShipments.map(row => ({ json: Object.fromEntries(cols.map((c,i) => [c, row[i]])) }));
'''.strip()

sample_data1 = code_node("Sample Shipment Data", sample_data_code, [40, 300])

audit_code = r'''
// EDIT THIS: your courier's contracted zone rate card (mirrors the Excel "Rate Card" tab)
const RATE_CARD = {
  A: { baseWeight: 0.5, baseRate: 35, addRate: 15, codPct: 0.02, codMin: 30, rtoPct: 1.0 },
  B: { baseWeight: 0.5, baseRate: 45, addRate: 20, codPct: 0.02, codMin: 30, rtoPct: 1.0 },
  C: { baseWeight: 0.5, baseRate: 55, addRate: 25, codPct: 0.02, codMin: 30, rtoPct: 1.0 },
  D: { baseWeight: 0.5, baseRate: 65, addRate: 30, codPct: 0.02, codMin: 30, rtoPct: 1.0 },
  E: { baseWeight: 0.5, baseRate: 95, addRate: 45, codPct: 0.02, codMin: 30, rtoPct: 1.0 },
};

function ceilToHalf(x) { return Math.ceil(x / 0.5) * 0.5; }

return $input.all().map(item => {
  const s = item.json;
  const rate = RATE_CARD[s.zone];
  const volumetricWeight = (s.length * s.width * s.height) / 5000;
  const chargeableWeight = ceilToHalf(Math.max(s.actualWeight, volumetricWeight));
  const extraUnits = Math.round((chargeableWeight - rate.baseWeight) / 0.5);
  const baseFreight = rate.baseRate;
  const additionalCharge = extraUnits * rate.addRate;
  const codCharge = s.paymentMode === "COD" ? Math.max(s.orderValue * rate.codPct, rate.codMin) : 0;
  const rtoCharge = s.status === "RTO" ? (baseFreight + additionalCharge) * rate.rtoPct : 0;
  const totalExpectedCharge = baseFreight + additionalCharge + codCharge + rtoCharge;
  const variance = Math.round((s.billedAmount - totalExpectedCharge) * 100) / 100;
  const verdict = variance > 1 ? "OVERCHARGED" : variance < -1 ? "UNDERBILLED" : "MATCH";
  return { json: { ...s, volumetricWeight, chargeableWeight, baseFreight, additionalCharge, codCharge, rtoCharge, totalExpectedCharge, variance, verdict } };
});
'''.strip()

audit1 = code_node("Audit Shipments", audit_code, [280, 300])

filter_code = 'return $input.all().filter(item => item.json.verdict === "OVERCHARGED");'
filter1 = code_node("Filter: Overcharged Only", filter_code, [560, 160])

summary_code = r'''
const items = $input.all().map(i => i.json);
const totalShipments = items.length;
const totalBilled = items.reduce((s,i)=>s+i.billedAmount,0);
const totalExpected = items.reduce((s,i)=>s+i.totalExpectedCharge,0);
const netVariance = Math.round((totalBilled - totalExpected) * 100) / 100;
const overcharged = items.filter(i=>i.verdict==="OVERCHARGED");
const underbilled = items.filter(i=>i.verdict==="UNDERBILLED");
const totalOvercharge = Math.round(overcharged.reduce((s,i)=>s+i.variance,0) * 100) / 100;
const zones = ["A","B","C","D","E"];
const zoneBreakdown = zones.map(z => {
  const zi = items.filter(i=>i.zone===z);
  return {
    zone: z,
    shipments: zi.length,
    totalBilled: zi.reduce((s,i)=>s+i.billedAmount,0),
    totalExpected: zi.reduce((s,i)=>s+i.totalExpectedCharge,0),
    overchargeAmount: Math.round(zi.filter(i=>i.verdict==="OVERCHARGED").reduce((s,i)=>s+i.variance,0) * 100) / 100,
  };
});
return [{ json: {
  totalShipmentsAudited: totalShipments,
  totalBilledByCourier: totalBilled,
  totalExpectedCharge: totalExpected,
  netVariance,
  shipmentsOvercharged: overcharged.length,
  totalOverchargeRefundClaimable: totalOvercharge,
  shipmentsUnderbilled: underbilled.length,
  zoneBreakdown,
}}];
'''.strip()

summary1 = code_node("Summary Dashboard", summary_code, [560, 440])

note1 = sticky(
    "## Courier Billing Audit\n\n"
    "Mirrors the Courier_Billing_Audit_Template.xlsx in this repo.\n\n"
    "1. Click **Execute workflow** to run it on the built-in sample data.\n"
    "2. Open **Audit Shipments** and edit the `RATE_CARD` object with your own courier's contracted rates.\n"
    "3. Replace **Sample Shipment Data** with a real source (Google Sheets, HTTP Request, or Read Binary File "
    "+ Extract from File for an uploaded .xlsx/.csv) - just keep the same field names.\n"
    "4. **Filter: Overcharged Only** outputs your dispute list. **Summary Dashboard** outputs the same "
    "totals as the Excel Summary Dashboard tab.",
    [-200, -40], width=760, height=220,
)

nodes1 = [trigger1, sample_data1, audit1, filter1, summary1, note1]
connections1 = merge_connections(
    chain("When clicking \"Execute workflow\"", "Sample Shipment Data", "Audit Shipments"),
    branch("Audit Shipments", ["Filter: Overcharged Only", "Summary Dashboard"]),
)
wf1 = workflow("Courier Billing Audit", nodes1, connections1)

with open(rf"{BASE}\courier-billing-audit\n8n-workflow\courier_billing_audit_workflow.json", "w", encoding="utf-8") as f:
    json.dump(wf1, f, indent=2)

print("saved workflow 1")


# ============================================================
# 2. Payment Gateway TDR Audit
# ============================================================

trigger2 = node("When clicking \"Execute workflow\"", "n8n-nodes-base.manualTrigger", {}, [-200, 300])

sample_data2_code = r'''
// Replace this node with your own data source (Google Sheets, HTTP Request, Read Binary File, etc.)
// Each item below matches one row of the "Settlement Data" tab in the Excel template.
const sampleSettlements = [
  ["TXN90001","ORD6001","UPI",1299,10.68,1.92,1286.40],
  ["TXN90002","ORD6002","Credit Card",2499,83.12,14.96,2400.92],
  ["TXN90003","ORD6003","Debit Card",899,3.60,0.64,894.76],
  ["TXN90004","ORD6004","Netbanking",1799,34.94,6.29,1757.77],
  ["TXN90005","ORD6005","Wallet",599,19.15,3.45,576.40],
  ["TXN90006","ORD6006","UPI",3499,10.50,1.89,3486.61],
  ["TXN90007","ORD6007","Credit Card",4299,128.23,23.08,4147.69],
  ["TXN90008","ORD6008","Debit Card",1099,17.11,3.08,1078.81],
  ["TXN90009","ORD6009","Netbanking",2199,43.18,7.77,2148.05],
  ["TXN90010","ORD6010","Wallet",1499,37.74,6.79,1454.47],
  ["TXN90011","ORD6011","UPI",999,2.15,0.39,996.46],
  ["TXN90012","ORD6012","Credit Card",5499,175.25,31.55,5292.20],
];
const cols = ["transactionId","orderId","paymentMethod","transactionAmount","actualTdrDeducted","actualGstDeducted","netSettledAmount"];
return sampleSettlements.map(row => ({ json: Object.fromEntries(cols.map((c,i) => [c, row[i]])) }));
'''.strip()

sample_data2 = code_node("Sample Settlement Data", sample_data2_code, [40, 300])

audit2_code = r'''
// EDIT THIS: your payment gateway's contracted TDR rate card (mirrors the Excel "TDR Rate Card" tab)
const RATE_CARD = {
  "UPI": { tdrRate: 0.003, gstRate: 0.18 },
  "Debit Card": { tdrRate: 0.004, gstRate: 0.18 },
  "Credit Card": { tdrRate: 0.018, gstRate: 0.18 },
  "Netbanking": { tdrRate: 0.010, gstRate: 0.18 },
  "Wallet": { tdrRate: 0.015, gstRate: 0.18 },
};

return $input.all().map(item => {
  const s = item.json;
  const rate = RATE_CARD[s.paymentMethod];
  const expectedTdrAmount = s.transactionAmount * rate.tdrRate;
  const expectedGstOnTdr = expectedTdrAmount * rate.gstRate;
  const expectedTotalDeduction = expectedTdrAmount + expectedGstOnTdr;
  const actualTotalDeduction = s.actualTdrDeducted + s.actualGstDeducted;
  const variance = Math.round((actualTotalDeduction - expectedTotalDeduction) * 100) / 100;
  const verdict = variance > 0.5 ? "OVERCHARGED" : variance < -0.5 ? "UNDERBILLED" : "MATCH";
  return { json: { ...s, expectedTdrRate: rate.tdrRate, expectedTdrAmount, expectedGstOnTdr, expectedTotalDeduction, actualTotalDeduction, variance, verdict } };
});
'''.strip()

audit2 = code_node("Audit Transactions", audit2_code, [280, 300])

filter2_code = 'return $input.all().filter(item => item.json.verdict === "OVERCHARGED");'
filter2 = code_node("Filter: Overcharged Only", filter2_code, [560, 160])

summary2_code = r'''
const items = $input.all().map(i => i.json);
const totalTransactions = items.length;
const totalTransactionValue = items.reduce((s,i)=>s+i.transactionAmount,0);
const totalActualDeduction = items.reduce((s,i)=>s+i.actualTotalDeduction,0);
const totalExpectedDeduction = items.reduce((s,i)=>s+i.expectedTotalDeduction,0);
const netVariance = Math.round((totalActualDeduction - totalExpectedDeduction) * 100) / 100;
const overcharged = items.filter(i=>i.verdict==="OVERCHARGED");
const underbilled = items.filter(i=>i.verdict==="UNDERBILLED");
const totalOvercharge = Math.round(overcharged.reduce((s,i)=>s+i.variance,0) * 100) / 100;
const methods = ["UPI","Debit Card","Credit Card","Netbanking","Wallet"];
const paymentMethodBreakdown = methods.map(m => {
  const mi = items.filter(i=>i.paymentMethod===m);
  return {
    paymentMethod: m,
    transactions: mi.length,
    totalDeducted: mi.reduce((s,i)=>s+i.actualTotalDeduction,0),
    totalExpected: mi.reduce((s,i)=>s+i.expectedTotalDeduction,0),
    overchargeAmount: Math.round(mi.filter(i=>i.verdict==="OVERCHARGED").reduce((s,i)=>s+i.variance,0) * 100) / 100,
  };
});
return [{ json: {
  totalTransactionsAudited: totalTransactions,
  totalTransactionValue,
  totalActualDeduction: Math.round(totalActualDeduction * 100) / 100,
  totalExpectedDeduction: Math.round(totalExpectedDeduction * 100) / 100,
  netVariance,
  transactionsOvercharged: overcharged.length,
  totalOverchargeRefundClaimable: totalOvercharge,
  transactionsUnderbilled: underbilled.length,
  paymentMethodBreakdown,
}}];
'''.strip()

summary2 = code_node("Summary Dashboard", summary2_code, [560, 440])

note2 = sticky(
    "## Payment Gateway TDR Audit\n\n"
    "Mirrors the Payment_Gateway_TDR_Audit_Template.xlsx in this repo.\n\n"
    "1. Click **Execute workflow** to run it on the built-in sample data.\n"
    "2. Open **Audit Transactions** and edit the `RATE_CARD` object with your own gateway's contracted "
    "TDR rates.\n"
    "3. Replace **Sample Settlement Data** with a real source (Google Sheets, HTTP Request, or Read Binary "
    "File + Extract from File for an uploaded .xlsx/.csv) - just keep the same field names.\n"
    "4. **Filter: Overcharged Only** outputs your dispute list. **Summary Dashboard** outputs the same "
    "totals as the Excel Summary Dashboard tab.",
    [-200, -40], width=760, height=220,
)

nodes2 = [trigger2, sample_data2, audit2, filter2, summary2, note2]
connections2 = merge_connections(
    chain("When clicking \"Execute workflow\"", "Sample Settlement Data", "Audit Transactions"),
    branch("Audit Transactions", ["Filter: Overcharged Only", "Summary Dashboard"]),
)
wf2 = workflow("Payment Gateway TDR Audit", nodes2, connections2)

with open(rf"{BASE}\payment-gateway-tdr-audit\n8n-workflow\payment_gateway_tdr_audit_workflow.json", "w", encoding="utf-8") as f:
    json.dump(wf2, f, indent=2)

print("saved workflow 2")


# ============================================================
# 3. Volumetric Weight & Box-Fit Checker
# ============================================================

trigger3 = node("When clicking \"Execute workflow\"", "n8n-nodes-base.manualTrigger", {}, [-200, 300])

box_library_code = r'''
// EDIT THIS: your own carton sizes, ordered smallest/cheapest to largest/costliest (mirrors the Excel "Box Library" tab)
const BOX_LIBRARY = [
  { code: "BX1", name: "XS", length: 15, width: 10, height: 8, maxWeight: 2, cost: 6 },
  { code: "BX2", name: "S", length: 20, width: 15, height: 10, maxWeight: 5, cost: 8 },
  { code: "BX3", name: "M", length: 25, width: 20, height: 15, maxWeight: 8, cost: 11 },
  { code: "BX4", name: "L", length: 35, width: 28, height: 18, maxWeight: 12, cost: 15 },
  { code: "BX5", name: "XL", length: 45, width: 35, height: 25, maxWeight: 20, cost: 22 },
];
return [{ json: { boxLibrary: BOX_LIBRARY } }];
'''.strip()

box_library3 = code_node("Box Library", box_library_code, [40, 300])

sample_products_code = r'''
// Replace this node with your own data source (Google Sheets, HTTP Request, Read Binary File, etc.)
// Each item below matches one row of the "Product Data" tab in the Excel template.
// Enter Length = longest side, Width = middle side, Height = shortest side.
const products = [
  ["SKU-1001","Face Serum 30ml",12,8,6,0.15],
  ["SKU-1002","Sunscreen Combo Pack",18,13,9,0.35],
  ["SKU-1003","Face Wash 100ml x2",16,11,7,0.40],
  ["SKU-1004","Moisturizer Jar Large",22,18,12,0.60],
  ["SKU-1005","Gift Hamper Small",24,19,14,1.20],
  ["SKU-1006","Gift Hamper Large",33,26,16,3.50],
  ["SKU-1007","Hair Dryer",30,14,10,0.90],
  ["SKU-1008","Combo Kit 6-pc",34,27,17,4.80],
  ["SKU-1009","Bulk Wholesale Carton",44,34,24,9.00],
  ["SKU-1010","Oversized Appliance",60,40,30,15.00],
];
const cols = ["sku","name","length","width","height","weight"];
return products.map(row => ({ json: Object.fromEntries(cols.map((c,i) => [c, row[i]])) }));
'''.strip()

sample_products3 = code_node("Sample Product Data", sample_products_code, [280, 300])

fit_code = r'''
const boxLibrary = $("Box Library").first().json.boxLibrary;

return $input.all().map(item => {
  const p = item.json;
  const productVolume = p.length * p.width * p.height;
  const fits = boxLibrary.filter(b =>
    p.length <= b.length && p.width <= b.width && p.height <= b.height && p.weight <= b.maxWeight
  );
  const recommended = fits[0]; // boxLibrary is ordered cheapest-first, so the first fit is the cheapest fit
  if (!recommended) {
    return { json: { ...p, productVolume, recommendedBox: "NO BOX FITS", recommendedBoxCost: 0, spaceUtilization: 0, status: "REVIEW - NO STANDARD BOX FITS" } };
  }
  const boxVolume = recommended.length * recommended.width * recommended.height;
  return { json: { ...p, productVolume, recommendedBox: recommended.code, recommendedBoxCost: recommended.cost, spaceUtilization: Math.round((productVolume / boxVolume) * 1000) / 1000, status: "OK" } };
});
'''.strip()

fit3 = code_node("Fit Checker", fit_code, [520, 300])

filter3_code = 'return $input.all().filter(item => item.json.status !== "OK");'
filter3 = code_node("Filter: Needs Review", filter3_code, [780, 160])

summary3_code = r'''
const items = $input.all().map(i => i.json);
const totalProducts = items.length;
const needsReview = items.filter(i => i.status !== "OK");
const fitted = items.filter(i => i.status === "OK");
const totalCost = fitted.reduce((s,i)=>s+i.recommendedBoxCost,0);
const avgUtilization = fitted.length ? Math.round((fitted.reduce((s,i)=>s+i.spaceUtilization,0) / fitted.length) * 1000) / 1000 : 0;
const boxCodes = ["BX1","BX2","BX3","BX4","BX5","NO BOX FITS"];
const boxUsageBreakdown = boxCodes.map(code => ({
  boxCode: code,
  productsAssigned: items.filter(i => i.recommendedBox === code).length,
}));
return [{ json: {
  totalProductsChecked: totalProducts,
  productsWithNoFittingBox: needsReview.length,
  totalRecommendedPackagingCost: totalCost,
  averageSpaceUtilization: avgUtilization,
  boxUsageBreakdown,
}}];
'''.strip()

summary3 = code_node("Summary", summary3_code, [780, 440])

note3 = sticky(
    "## Volumetric Weight & Box-Fit Checker\n\n"
    "Mirrors the Volumetric_Weight_Box_Fit_Checker.xlsx in this repo.\n\n"
    "1. Click **Execute workflow** to run it on the built-in sample data.\n"
    "2. Open **Box Library** and edit `BOX_LIBRARY` with your own carton sizes - keep them ordered "
    "smallest/cheapest to largest/costliest.\n"
    "3. Replace **Sample Product Data** with a real source (Google Sheets, HTTP Request, or Read Binary "
    "File + Extract from File for an uploaded .xlsx/.csv). Enter Length = longest side, Width = middle "
    "side, Height = shortest side.\n"
    "4. **Filter: Needs Review** outputs products with no fitting box. **Summary** outputs the same totals "
    "as the Excel Summary tab.",
    [-200, -60], width=780, height=240,
)

nodes3 = [trigger3, box_library3, sample_products3, fit3, filter3, summary3, note3]
connections3 = merge_connections(
    chain("When clicking \"Execute workflow\"", "Box Library", "Sample Product Data", "Fit Checker"),
    branch("Fit Checker", ["Filter: Needs Review", "Summary"]),
)
wf3 = workflow("Volumetric Weight & Box-Fit Checker", nodes3, connections3)

with open(rf"{BASE}\volumetric-weight-box-fit-checker\n8n-workflow\box_fit_checker_workflow.json", "w", encoding="utf-8") as f:
    json.dump(wf3, f, indent=2)

print("saved workflow 3")
