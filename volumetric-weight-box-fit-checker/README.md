# Volumetric Weight & Box-Fit Checker

**The problem:** Couriers charge by volumetric weight, not just actual weight - so shipping a product in a
box that's bigger than it needs to be can quietly inflate every shipping bill. And packing teams often
figure out a product doesn't fit its usual box only after it's already been picked.

**What this template does:** You give it your standard box sizes and your product dimensions. It tells you
the cheapest box each product actually fits in, and flags any product that doesn't fit any box you stock -
before it becomes a packing-table problem or an oversized shipping bill.

## File

[`Volumetric_Weight_Box_Fit_Checker.xlsx`](./Volumetric_Weight_Box_Fit_Checker.xlsx)

## Tabs in the workbook

1. **Read Me** - quick instructions.
2. **Box Library** - your standard carton sizes, max weight capacity, and cost per box. Sample values
   included - replace with your own packaging.
3. **Product Data** - paste your own product dimensions and weights here.
4. **Fit Checker** - checks each product against every box and recommends the cheapest one that fits, or
   flags "NO BOX FITS" if none do.
5. **Summary** - how many products need review, total recommended packaging cost, and box usage breakdown.

## Important: how to enter dimensions

For **every product and every box**, enter:
- **Length** = the longest side
- **Width** = the middle side
- **Height** = the shortest side

This keeps the fit-check accurate no matter which way something is actually oriented. Also keep the Box
Library ordered from smallest/cheapest to largest/costliest - the checker recommends the first box that
fits, which only works out to the cheapest option if the sizes are in ascending order.

## Before you use it

Replace the 5 sample box sizes (XS to XL) and their costs with your actual packaging options, and swap in
your real product catalog on the Product Data tab.
