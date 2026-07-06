# Courier Billing Audit Template

**The problem:** Couriers bill you per shipment based on zone, weight, and delivery type (prepaid, COD,
RTO). Mistakes - a shipment billed in the wrong zone, weight rounded up to the wrong slab, a COD or RTO
charge applied incorrectly - are common, and reviewing hundreds of shipments by hand isn't realistic.
Most brands just pay the bill without checking.

**What this template does:** You give it your rate card and your shipment data. It calculates what each
shipment *should* have cost, compares it to what the courier actually billed, and flags every mismatch -
so you end up with a ready-made list of overcharges to dispute.

## File

[`Courier_Billing_Audit_Template.xlsx`](./Courier_Billing_Audit_Template.xlsx)

## What it looks like

**Rate Card** - your zone rates, ready to overwrite:

![Rate Card](./screenshots/rate-card.png)

**Audit** - every shipment checked, overcharges flagged automatically:

![Audit](./screenshots/audit.png)

**Summary Dashboard** - your refund claim total, broken down by zone:

![Summary Dashboard](./screenshots/summary-dashboard.png)

## Tabs in the workbook

1. **Read Me** - quick instructions.
2. **Rate Card** - your zone-wise rates (base rate, per-0.5kg rate, COD %, RTO %). Sample values included -
   replace with your actual courier contract.
3. **Shipment Data** - paste your own shipment export here (AWB, zone, weight, dimensions, payment mode,
   status, what the courier billed).
4. **Audit** - calculates volumetric weight, chargeable weight, and the expected charge for every shipment,
   then compares it to the billed amount. Verdict column shows MATCH, OVERCHARGED, or UNDERBILLED.
5. **Summary Dashboard** - total overcharge amount (your refund claim), plus a zone-wise breakdown.

## How the math works

- **Volumetric weight** = (Length x Width x Height in cm) / 5000
- **Chargeable weight** = the higher of actual weight and volumetric weight, rounded up to the nearest 0.5 kg
- **Expected charge** = base freight (by zone) + extra weight charge + COD charge (if applicable) + RTO
  charge (if the shipment was returned)
- **Variance** = what the courier billed minus what you expected to be billed. Positive = you were
  overcharged.

## Step-by-step walkthrough (worked example)

The template ships pre-loaded with 12 sample shipments so you can see it work before touching your own data.
Here's what happens end to end, using shipment **AWB1001** as the example:

1. **Set up your rate card first.** Open the Rate Card tab. Zone A ("Local, Same City") is set up as:
   base rate Rs 35 for the first 0.5 kg, plus Rs 15 for every additional 0.5 kg, 2% COD charge (Rs 30
   minimum), and a 100% RTO surcharge on the forward freight if the shipment bounces back. Replace these
   five zones with your own courier's actual rate card - the rest of the workbook reads from this tab, so
   nothing else needs to change.

2. **Drop in your shipment data.** On the Shipment Data tab, AWB1001 is a Zone A, Prepaid shipment: actual
   weight 0.40 kg, dimensions 20x15x10 cm, delivered, and the courier billed Rs 75 for it. This is exactly
   the kind of row you'd paste in from your own courier's monthly billing export.

3. **The Audit tab does the work automatically.** For AWB1001, it calculates:
   - Volumetric weight = (20 x 15 x 10) / 5000 = **0.60 kg**
   - Chargeable weight = higher of actual (0.40) and volumetric (0.60), rounded up to the nearest 0.5 kg =
     **1.00 kg**
   - Expected base freight (Zone A, first 0.5 kg) = **Rs 35**
   - Expected additional weight charge (1 extra 0.5 kg slab x Rs 15) = **Rs 15**
   - No COD or RTO charge applies (Prepaid, Delivered)
   - **Total expected charge = Rs 50**
   - Billed by courier = **Rs 75** → **Variance = Rs 25** → Verdict: **OVERCHARGED**

   Scan down the Audit tab and you'll see this repeats for every row - 9 of the 12 sample shipments come
   back overcharged, 2 match exactly, and 1 was actually underbilled.

4. **Read the total off the Summary Dashboard.** For the sample data, that's **Rs 323 in total overcharges**
   across 9 shipments - broken down by zone, so you know exactly which zone to raise with your courier first.

5. **Swap in your real data** on the Rate Card and Shipment Data tabs (delete the sample rows first), and
   the Audit and Summary Dashboard tabs recalculate instantly - no formulas to touch.

## Before you use it

Replace the sample rate card (5 generic zones: Local, Regional, Metro-to-Metro, Rest of India, Special/NE)
with your own courier's actual contracted rates. Zone names and structure are illustrative - adjust to match
however your courier defines zones.

## Use cases

- **Monthly invoice reconciliation** - check every courier bill before you pay it, not after.
- **Multi-courier comparison** - run the same shipment data through different couriers' rate cards to see
  who's actually cheapest.
- **Vendor negotiation leverage** - a documented pattern of overcharges (by zone, by weight slab) is hard
  evidence when renegotiating a contract.
- **RTO cost audits** - RTO charges are often billed incorrectly and rarely checked line-by-line.
- **Onboarding a new courier/3PL** - validate their first month of billing against the agreed contract
  before trusting them long-term.
