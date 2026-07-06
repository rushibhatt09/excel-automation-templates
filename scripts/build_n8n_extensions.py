import sys
sys.path.insert(0, r"C:\Users\micro\OneDrive\Documents\excel-automation-templates\scripts")
from n8n_helpers import node, code_node, sticky, chain, branch, merge_connections, workflow, save_workflow

BASE = r"C:\Users\micro\OneDrive\Documents\excel-automation-templates"

# ============================================================
# Extension 1: Courier Billing Audit -> Dispute Email Drafter
# ============================================================

trigger_a = node("When clicking \"Execute workflow\"", "n8n-nodes-base.manualTrigger", {}, [-200, 300])

sample_overcharges_a = code_node("Sample Overcharged Shipments", r'''
// This is normally the "Filter: Overcharged Only" output from the Courier Billing Audit workflow.
// Sample cases below match what that workflow finds on its own sample data.
const overcharges = [
  { awb: "AWB1001", zone: "A", billedAmount: 75, totalExpectedCharge: 50, variance: 25 },
  { awb: "AWB1003", zone: "C", billedAmount: 173, totalExpectedCharge: 155, variance: 18 },
  { awb: "AWB1004", zone: "D", billedAmount: 200, totalExpectedCharge: 160, variance: 40 },
  { awb: "AWB1005", zone: "E", billedAmount: 560, totalExpectedCharge: 500, variance: 60 },
];
return overcharges.map(o => ({ json: o }));
'''.strip(), [40, 300])

draft_individual_a = code_node("Draft Individual Dispute Emails", r'''
return $input.all().map(item => {
  const s = item.json;
  const subject = `Billing Dispute - ${s.awb} - Zone ${s.zone} Overcharge of Rs ${s.variance}`;
  const body = `Hi Team,\n\nWe've identified a billing discrepancy on shipment ${s.awb} (Zone ${s.zone}):\n` +
    `- Billed Amount: Rs ${s.billedAmount}\n` +
    `- Expected Amount (per our contracted rate card): Rs ${s.totalExpectedCharge}\n` +
    `- Overcharge: Rs ${s.variance}\n\n` +
    `Please review and process a refund/credit for the difference.\n\nThanks,\n[Your Name]`;
  return { json: { ...s, emailSubject: subject, emailBody: body } };
});
'''.strip(), [340, 160])

draft_consolidated_a = code_node("Draft Consolidated Dispute Email", r'''
const items = $input.all().map(i => i.json);
const totalOvercharge = Math.round(items.reduce((s,i)=>s+i.variance,0) * 100) / 100;
const lines = items.map(i => `- ${i.awb} (Zone ${i.zone}): Billed Rs ${i.billedAmount}, Expected Rs ${i.totalExpectedCharge}, Overcharge Rs ${i.variance}`).join('\n');
const subject = `Monthly Billing Dispute - ${items.length} Overcharged Shipments - Rs ${totalOvercharge} Refund Requested`;
const body = `Hi Team,\n\nOur monthly billing audit found ${items.length} shipments overcharged, totaling Rs ${totalOvercharge} in disputed charges:\n\n${lines}\n\nPlease review and process a refund/credit for the total overcharge amount.\n\nThanks,\n[Your Name]`;
return [{ json: { emailSubject: subject, emailBody: body, totalCases: items.length, totalOvercharge } }];
'''.strip(), [340, 440])

note_a = sticky(
    "## Courier Dispute Email Drafter\n\n"
    "Takes the overcharged-shipment list (from the Courier Billing Audit workflow's "
    "\"Filter: Overcharged Only\" output) and drafts dispute email text - one per shipment, plus one "
    "consolidated monthly email.\n\n"
    "1. Replace **Sample Overcharged Shipments** with the real output of the audit workflow (or a "
    "Google Sheets/HTTP node reading your own flagged list).\n"
    "2. Connect a **Gmail/Outlook/SMTP** node after either drafting node to actually send - this workflow "
    "only drafts, it never sends anything on its own.",
    [-200, -60], width=760, height=200,
)

nodes_a = [trigger_a, sample_overcharges_a, draft_individual_a, draft_consolidated_a, note_a]
connections_a = merge_connections(
    chain("When clicking \"Execute workflow\"", "Sample Overcharged Shipments"),
    branch("Sample Overcharged Shipments", ["Draft Individual Dispute Emails", "Draft Consolidated Dispute Email"]),
)
wf_a = workflow("Courier Billing Audit - Dispute Email Drafter", nodes_a, connections_a)
save_workflow(wf_a, rf"{BASE}\courier-billing-audit\n8n-workflow\dispute_email_drafter_workflow.json")
print("saved extension 1")


# ============================================================
# Extension 2: Payment Gateway TDR Audit -> Dispute Email Drafter
# ============================================================

trigger_b = node("When clicking \"Execute workflow\"", "n8n-nodes-base.manualTrigger", {}, [-200, 300])

sample_overcharges_b = code_node("Sample Overcharged Transactions", r'''
// This is normally the "Filter: Overcharged Only" output from the Payment Gateway TDR Audit workflow.
// Sample cases below match what that workflow finds on its own sample data.
const overcharges = [
  { transactionId: "TXN90001", paymentMethod: "UPI", actualTotalDeduction: 12.60, expectedTotalDeduction: 4.60, variance: 8.00 },
  { transactionId: "TXN90002", paymentMethod: "Credit Card", actualTotalDeduction: 98.08, expectedTotalDeduction: 53.08, variance: 45.00 },
  { transactionId: "TXN90007", paymentMethod: "Credit Card", actualTotalDeduction: 151.31, expectedTotalDeduction: 91.31, variance: 60.00 },
  { transactionId: "TXN90012", paymentMethod: "Credit Card", actualTotalDeduction: 206.80, expectedTotalDeduction: 116.80, variance: 90.00 },
];
return overcharges.map(o => ({ json: o }));
'''.strip(), [40, 300])

draft_individual_b = code_node("Draft Individual Dispute Emails", r'''
return $input.all().map(item => {
  const s = item.json;
  const subject = `Settlement Dispute - ${s.transactionId} - ${s.paymentMethod} Overcharge of Rs ${s.variance}`;
  const body = `Hi Team,\n\nWe've identified a settlement discrepancy on transaction ${s.transactionId} (${s.paymentMethod}):\n` +
    `- Actual Deduction: Rs ${s.actualTotalDeduction}\n` +
    `- Expected Deduction (per our contracted TDR rate): Rs ${s.expectedTotalDeduction}\n` +
    `- Overcharge: Rs ${s.variance}\n\n` +
    `Please review and process a refund/credit for the difference.\n\nThanks,\n[Your Name]`;
  return { json: { ...s, emailSubject: subject, emailBody: body } };
});
'''.strip(), [340, 160])

draft_consolidated_b = code_node("Draft Consolidated Dispute Email", r'''
const items = $input.all().map(i => i.json);
const totalOvercharge = Math.round(items.reduce((s,i)=>s+i.variance,0) * 100) / 100;
const lines = items.map(i => `- ${i.transactionId} (${i.paymentMethod}): Actual Rs ${i.actualTotalDeduction}, Expected Rs ${i.expectedTotalDeduction}, Overcharge Rs ${i.variance}`).join('\n');
const subject = `Monthly Settlement Dispute - ${items.length} Overcharged Transactions - Rs ${totalOvercharge} Refund Requested`;
const body = `Hi Team,\n\nOur monthly settlement audit found ${items.length} transactions overcharged, totaling Rs ${totalOvercharge} in disputed deductions:\n\n${lines}\n\nPlease review and process a refund/credit for the total overcharge amount.\n\nThanks,\n[Your Name]`;
return [{ json: { emailSubject: subject, emailBody: body, totalCases: items.length, totalOvercharge } }];
'''.strip(), [340, 440])

note_b = sticky(
    "## Payment Gateway Dispute Email Drafter\n\n"
    "Takes the overcharged-transaction list (from the Payment Gateway TDR Audit workflow's "
    "\"Filter: Overcharged Only\" output) and drafts dispute email text - one per transaction, plus one "
    "consolidated monthly email.\n\n"
    "1. Replace **Sample Overcharged Transactions** with the real output of the audit workflow (or a "
    "Google Sheets/HTTP node reading your own flagged list).\n"
    "2. Connect a **Gmail/Outlook/SMTP** node after either drafting node to actually send - this workflow "
    "only drafts, it never sends anything on its own.",
    [-200, -60], width=760, height=200,
)

nodes_b = [trigger_b, sample_overcharges_b, draft_individual_b, draft_consolidated_b, note_b]
connections_b = merge_connections(
    chain("When clicking \"Execute workflow\"", "Sample Overcharged Transactions"),
    branch("Sample Overcharged Transactions", ["Draft Individual Dispute Emails", "Draft Consolidated Dispute Email"]),
)
wf_b = workflow("Payment Gateway TDR Audit - Dispute Email Drafter", nodes_b, connections_b)
save_workflow(wf_b, rf"{BASE}\payment-gateway-tdr-audit\n8n-workflow\dispute_email_drafter_workflow.json")
print("saved extension 2")


# ============================================================
# Extension 3: Box-Fit Checker -> Packaging Review Notice Drafter
# (Adapted from "dispute email" since there's no external vendor to dispute with here -
#  this is an internal notice to the packaging/procurement team instead.)
# ============================================================

trigger_c = node("When clicking \"Execute workflow\"", "n8n-nodes-base.manualTrigger", {}, [-200, 300])

sample_noboxfits_c = code_node("Sample No-Fit Products", r'''
// This is normally the "Filter: Needs Review" output from the Box-Fit Checker workflow.
const noFits = [
  { sku: "SKU-1010", name: "Oversized Appliance", length: 60, width: 40, height: 30, weight: 15 },
];
return noFits.map(o => ({ json: o }));
'''.strip(), [40, 300])

draft_individual_c = code_node("Draft Individual Review Notices", r'''
return $input.all().map(item => {
  const s = item.json;
  const subject = `Packaging Review Needed - ${s.sku} - No Standard Box Fits`;
  const body = `Hi Team,\n\n${s.name} (SKU ${s.sku}, ${s.length}x${s.width}x${s.height} cm, ${s.weight} kg) does not fit ` +
    `any box in our current packaging library.\n\n` +
    `Please either source a custom box for this SKU or confirm an alternate shipping method.\n\nThanks,\n[Your Name]`;
  return { json: { ...s, noticeSubject: subject, noticeBody: body } };
});
'''.strip(), [340, 160])

draft_consolidated_c = code_node("Draft Consolidated Review Notice", r'''
const items = $input.all().map(i => i.json);
const lines = items.map(i => `- ${i.sku} (${i.name}): ${i.length}x${i.width}x${i.height} cm, ${i.weight} kg`).join('\n');
const subject = `Packaging Review Needed - ${items.length} Product(s) With No Standard Box Fit`;
const body = `Hi Team,\n\nThis run of the Box-Fit Checker found ${items.length} product(s) that don't fit any box in our packaging library:\n\n${lines}\n\nPlease review and either source custom boxes or confirm alternate shipping for these SKUs.\n\nThanks,\n[Your Name]`;
return [{ json: { noticeSubject: subject, noticeBody: body, totalCases: items.length } }];
'''.strip(), [340, 440])

note_c = sticky(
    "## Packaging Review Notice Drafter\n\n"
    "Takes the no-fit product list (from the Box-Fit Checker workflow's \"Filter: Needs Review\" output) "
    "and drafts an internal notice for your packaging/procurement team - one per product, plus one "
    "consolidated notice. This is an internal alert, not a vendor dispute (there's no vendor to dispute "
    "with for a packaging-fit issue).\n\n"
    "1. Replace **Sample No-Fit Products** with the real output of the Box-Fit Checker workflow.\n"
    "2. Connect a **Slack/Email/Teams** node after either drafting node to actually send it.",
    [-200, -60], width=760, height=220,
)

nodes_c = [trigger_c, sample_noboxfits_c, draft_individual_c, draft_consolidated_c, note_c]
connections_c = merge_connections(
    chain("When clicking \"Execute workflow\"", "Sample No-Fit Products"),
    branch("Sample No-Fit Products", ["Draft Individual Review Notices", "Draft Consolidated Review Notice"]),
)
wf_c = workflow("Box-Fit Checker - Packaging Review Notice Drafter", nodes_c, connections_c)
save_workflow(wf_c, rf"{BASE}\volumetric-weight-box-fit-checker\n8n-workflow\packaging_review_notice_workflow.json")
print("saved extension 3")
