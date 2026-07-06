# Payment Gateway TDR Settlement Audit Template

**The problem:** Payment gateways deduct a TDR (Transaction Discount Rate) plus GST from every transaction
before settling the rest to you. The rate depends on payment method (UPI, cards, netbanking, wallets), and
gateways occasionally deduct more than the contracted rate - a few rupees at a time, across thousands of
transactions, which adds up and is easy to miss.

**What this template does:** You give it your contracted TDR rates and your settlement data. It calculates
what should have been deducted for every transaction, compares it to what was actually deducted, and flags
every overcharge.

## File

[`Payment_Gateway_TDR_Audit_Template.xlsx`](./Payment_Gateway_TDR_Audit_Template.xlsx)

Prefer automation over spreadsheets? The same audit logic is also available as a ready-to-import
[n8n workflow](./n8n-workflow) - same rate card, same math, same sample results.

## What it looks like

**TDR Rate Card** - your contracted rates by payment method:

![TDR Rate Card](./screenshots/rate-card.png)

**Audit** - every transaction checked, overcharges flagged automatically:

![Audit](./screenshots/audit.png)

**Summary Dashboard** - your refund claim total, broken down by payment method:

![Summary Dashboard](./screenshots/summary-dashboard.png)

## Tabs in the workbook

1. **Read Me** - quick instructions.
2. **TDR Rate Card** - your contracted TDR % and GST % by payment method. Sample values included - replace
   with your actual gateway contract.
3. **Settlement Data** - paste your own settlement export here (transaction ID, payment method, amount,
   TDR deducted, GST deducted, net settled).
4. **Audit** - calculates the expected TDR, expected GST, and expected total deduction for every
   transaction, then compares it to what was actually deducted. Verdict column shows MATCH, OVERCHARGED,
   or UNDERBILLED.
5. **Summary Dashboard** - total overcharge amount (your refund claim), plus a payment-method breakdown.

## How the math works

- **Expected TDR** = Transaction Amount x contracted TDR rate for that payment method
- **Expected GST** = Expected TDR x GST rate (GST applies on the TDR amount, not the transaction amount)
- **Expected total deduction** = Expected TDR + Expected GST
- **Variance** = actual total deduction minus expected total deduction. Positive = you were overcharged.

## Step-by-step walkthrough (worked example)

The template ships pre-loaded with 12 sample transactions so you can see it work before touching your own
data. Here's what happens end to end, using transaction **TXN90001** as the example:

1. **Set up your TDR rate card first.** Open the TDR Rate Card tab. UPI is set up as 0.30% TDR plus 18% GST
   on that TDR. Replace these five payment methods with your own gateway's actual contracted rates - the
   rest of the workbook reads from this tab, so nothing else needs to change.

2. **Drop in your settlement data.** On the Settlement Data tab, TXN90001 is a UPI transaction for
   Rs 1,299, where the gateway deducted Rs 10.68 TDR + Rs 1.92 GST. This is exactly the kind of row you'd
   paste in from your own gateway's settlement report.

3. **The Audit tab does the work automatically.** For TXN90001, it calculates:
   - Expected TDR = Rs 1,299 x 0.30% = **Rs 3.90**
   - Expected GST on that TDR = Rs 3.90 x 18% = **Rs 0.70**
   - **Total expected deduction = Rs 4.60**
   - Actual deducted by gateway = Rs 10.68 + Rs 1.92 = **Rs 12.60** → **Variance = Rs 8.00** → Verdict:
     **OVERCHARGED**

   Scan down the Audit tab and you'll see this repeats for every row - 9 of the 12 sample transactions come
   back overcharged, 2 match exactly, and 1 was actually underbilled.

4. **Read the total off the Summary Dashboard.** For the sample data, that's **Rs 293 in total overcharges**
   across 9 transactions - broken down by payment method, so you know exactly which payment method to raise
   with your gateway first.

5. **Swap in your real data** on the TDR Rate Card and Settlement Data tabs (delete the sample rows first),
   and the Audit and Summary Dashboard tabs recalculate instantly - no formulas to touch.

## Before you use it

Replace the sample TDR rate card (UPI, Debit Card, Credit Card, Netbanking, Wallet) with your own gateway's
actual contracted rates - these vary a lot by provider and by your negotiated merchant agreement.

The Audit and Summary Dashboard formulas are pre-built for up to 200 transactions - paste in fewer or more
rows and the totals adjust automatically, no formulas to touch. If you have more than 200 transactions,
select the last row of the Audit tab and drag-fill it down as far as you need.

## Use cases

- **Monthly settlement reconciliation** - catch gateway overcharges before small per-transaction deductions
  compound across thousands of transactions.
- **Comparing gateways** - run the same transaction mix through multiple providers' rate cards to see true
  cost per payment method.
- **UPI/MDR compliance checks** - flag cases where a gateway is charging TDR on payment methods that should
  be zero-cost under regulation (e.g. UPI).
- **Renewal negotiations** - quantify actual overcharge history as evidence when renegotiating merchant
  rates.
