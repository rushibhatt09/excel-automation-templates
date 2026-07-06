# Excel Automation Templates

Free, no-code Excel/Google Sheets templates for the spreadsheet work that admin, ops, and finance folks
end up doing by hand every month - checking bills, catching overcharges, and making sure the numbers add up.

No coding, no plugins, no sign-ups. Download a template, drop in your own data, and the formulas do the rest.

## Templates

Every template follows the same pattern: a Rate Card/Library tab you customize, a Data tab you paste your
own records into, and an Audit/Fit Checker tab that recalculates automatically and flags what needs
attention.

### 1. [Courier Billing Audit](./courier-billing-audit)

Catches courier/logistics overcharges - wrong zone, wrong weight slab, inflated COD/RTO charges. Feed it
your rate card and shipment data; it flags every mismatch and totals up your refund claim.

![Courier Billing Audit - Audit tab](./courier-billing-audit/screenshots/audit.png)

In the sample data: **9 of 12 shipments overcharged, ₹323 in refund-claimable overcharges**, broken down by
zone. Full screenshots (Rate Card, Audit, Summary Dashboard) and a worked example walking through the math
row-by-row are in the [template README](./courier-billing-audit/README.md).

### 2. [Payment Gateway TDR Audit](./payment-gateway-tdr-audit)

Catches payment gateway settlement overcharges against your contracted TDR (Transaction Discount Rate) rate
card. Feed it your rate card and settlement data; it flags every transaction where more was deducted than
agreed.

![Payment Gateway TDR Audit - Audit tab](./payment-gateway-tdr-audit/screenshots/audit.png)

In the sample data: **9 of 12 transactions overcharged, ₹293 in refund-claimable overcharges**, broken down
by payment method. Full screenshots (TDR Rate Card, Audit, Summary Dashboard) and a worked example are in
the [template README](./payment-gateway-tdr-audit/README.md).

### 3. [Volumetric Weight & Box-Fit Checker](./volumetric-weight-box-fit-checker)

Tells you the cheapest box each product actually fits in, and flags products with no good fit - before it
becomes a packing-table problem or an oversized shipping bill.

![Box-Fit Checker - Fit Checker tab](./volumetric-weight-box-fit-checker/screenshots/fit-checker.png)

In the sample data: **10 products checked, 1 flagged for review, ₹111 total recommended packaging cost**.
Full screenshots (Box Library, Fit Checker, Summary) and a worked example are in the
[template README](./volumetric-weight-box-fit-checker/README.md).

## How to use any template

1. Open the template folder and download the `.xlsx` file.
2. Open it in Excel or upload it to Google Sheets.
3. Every workbook has a **Read Me** tab first - follow its steps.
4. Replace the sample data (blue text, yellow-shaded cells) with your own numbers.
5. The audit/summary tabs recalculate automatically - no formulas to write yourself.

## Use cases

- **Reconciliation** - check courier bills and payment gateway settlements before you pay/accept them, not after.
- **Vendor negotiation** - a documented pattern of overcharges is real leverage when renegotiating contracts or rates.
- **Onboarding new vendors** - validate a new courier's or gateway's first month of billing against the agreed contract.
- **Packaging/warehouse planning** - avoid oversized boxes and packing-table surprises before a product launches.
- **Portfolio/consulting proof** - hand a prospective employer or client a working template instead of just describing the skill.

Each template's own README has a more detailed use-case list for that specific workflow.

## Why these exist

Built out of real operational work auditing courier billing and payment settlements for an e-commerce
brand - turned into generic templates anyone can reuse, with all company-specific data stripped out and
replaced with illustrative sample numbers.

## License

MIT - use, modify, and share freely.
