import argparse
import json
import pandas as pd
from billing_audit.audit import audit

def main():
    parser = argparse.ArgumentParser(description="Billing discrepancy auditor (CSV).")
    parser.add_argument("--invoices", required=True, help="Path to invoices CSV")
    parser.add_argument("--line-items", required=True, help="Path to line items CSV")
    parser.add_argument("--out-csv", default="report.csv", help="Output CSV report path")
    parser.add_argument("--out-json", default="report.json", help="Output JSON report path")
    parser.add_argument("--tolerance", type=float, default=0.01, help="Tolerance for total comparisons")
    args = parser.parse_args()

    invoices = pd.read_csv(args.invoices)
    line_items = pd.read_csv(args.line_items)

    discrepancies = audit(invoices, line_items, tol=args.tolerance)

    rows = [
        {
            "invoice_id": d.invoice_id,
            "issue": d.issue,
            "expected": d.expected,
            "actual": d.actual,
        }
        for d in discrepancies
    ]

    df = pd.DataFrame(rows).sort_values(["invoice_id", "issue"]) if rows else pd.DataFrame(rows)
    df.to_csv(args.out_csv, index=False)

    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

    # Console summary
    print(f"Discrepancies found: {len(rows)}")
    if len(rows) > 0:
        print(df.head(20).to_string(index=False))

if __name__ == "__main__":
    main()
