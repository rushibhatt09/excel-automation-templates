import win32com.client
import os
import time

BASE = r"C:\Users\micro\OneDrive\Documents\excel-automation-templates"

JOBS = [
    (f"{BASE}\\courier-billing-audit\\Courier_Billing_Audit_Template.xlsx", [
        ("Rate Card", "A1:H11", f"{BASE}\\courier-billing-audit\\screenshots\\rate-card.png"),
        ("Audit", "A1:Q14", f"{BASE}\\courier-billing-audit\\screenshots\\audit.png"),
        ("Summary Dashboard", "B2:F19", f"{BASE}\\courier-billing-audit\\screenshots\\summary-dashboard.png"),
    ]),
    (f"{BASE}\\payment-gateway-tdr-audit\\Payment_Gateway_TDR_Audit_Template.xlsx", [
        ("TDR Rate Card", "A1:G13", f"{BASE}\\payment-gateway-tdr-audit\\screenshots\\rate-card.png"),
        ("Audit", "A1:L13", f"{BASE}\\payment-gateway-tdr-audit\\screenshots\\audit.png"),
        ("Summary Dashboard", "B2:F20", f"{BASE}\\payment-gateway-tdr-audit\\screenshots\\summary-dashboard.png"),
    ]),
    (f"{BASE}\\volumetric-weight-box-fit-checker\\Volumetric_Weight_Box_Fit_Checker.xlsx", [
        ("Box Library", "A1:H11", f"{BASE}\\volumetric-weight-box-fit-checker\\screenshots\\box-library.png"),
        ("Fit Checker", "A1:P11", f"{BASE}\\volumetric-weight-box-fit-checker\\screenshots\\fit-checker.png"),
        ("Summary", "B2:D17", f"{BASE}\\volumetric-weight-box-fit-checker\\screenshots\\summary.png"),
    ]),
]

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
excel.DisplayAlerts = False

xlScreen = 1
xlBitmap = 2

for path, sheets in JOBS:
    wb = excel.Workbooks.Open(path)
    excel.CalculateFullRebuild()
    excel.CalculateUntilAsyncQueriesDone()
    for sheet_name, rng_addr, out_path in sheets:
        ws = wb.Sheets(sheet_name)
        ws.Activate()
        rng = ws.Range(rng_addr)
        excel.ActiveWindow.ScrollRow = rng.Row
        excel.ActiveWindow.ScrollColumn = 1
        rng.Select()
        time.sleep(0.5)
        rng.CopyPicture(Appearance=xlScreen, Format=xlBitmap)
        time.sleep(0.5)
        w = rng.Width * 1.6
        h = rng.Height * 1.6
        co = ws.ChartObjects().Add(0, 0, w, h)
        co.Chart.Paste()
        time.sleep(0.5)
        co.Chart.Export(out_path, "PNG")
        co.Delete()
        print("saved", out_path)
    wb.Close(SaveChanges=False)

excel.Quit()
print("done")
