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

## Before you use it

Replace the sample TDR rate card (UPI, Debit Card, Credit Card, Netbanking, Wallet) with your own gateway's
actual contracted rates - these vary a lot by provider and by your negotiated merchant agreement.

## Use cases

- **Monthly settlement reconciliation** - catch gateway overcharges before small per-transaction deductions
  compound across thousands of transactions.
- **Comparing gateways** - run the same transaction mix through multiple providers' rate cards to see true
  cost per payment method.
- **UPI/MDR compliance checks** - flag cases where a gateway is charging TDR on payment methods that should
  be zero-cost under regulation (e.g. UPI).
- **Renewal negotiations** - quantify actual overcharge history as evidence when renegotiating merchant
  rates.
