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
