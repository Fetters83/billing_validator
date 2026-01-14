from dataclasses import dataclass
import pandas as pd


@dataclass
class Discrepancy:
    invoice_id: str
    issue: str
    expected: float | None
    actual: float | None


def audit(invoices: pd.DataFrame, line_items:pd.DataFrame,tol: float = 0.01) -> list[Discrepancy]:
    discrepancies: list[Discrepancy] = []

    li_sum = (
        line_items.groupby("invoice_id",as_index=False)["line_total"]
        .sum()
        .rename(columns={"line_total":"line_items_total"})

    )

    merged = invoices.merge(li_sum, on="invoice_id",how="left")
    merged["line_items_total"] = merged["line_items_total"].fillna(0.0)

    diff = (merged["invoice_total"] - merged["line_items_total"]).abs()
    mismatches = merged[diff > tol]
    for row in mismatches.itertuples(index=False):
        discrepancies.append(
            Discrepancy(
                invoice_id=row.invoice_id,
                issue="TOTAL_MISMATCH",
                expected=float(row.invoice_total),
                actual=float(row.line_items_total),

            )
        )
    missing = merged[(merged["line_items_total"] == 0) & (merged["invoice_total"].abs() > tol)]
    for row in missing.itertuples(index=False):
        discrepancies.append(
            Discrepancy(
                invoice_id=row.invoice_id,
                issue="MISSING_LINE_ITEMS",
                expected=float(row.invoice_total),
                actual=float(row.line_items_total),
            )
        )

    # 3) negative totals
    negative = invoices[invoices["invoice_total"] < -tol]
    for row in negative.itertuples(index=False):
        discrepancies.append(
            Discrepancy(
                invoice_id=row.invoice_id,
                issue="NEGATIVE_INVOICE_TOTAL",
                expected=None,
                actual=float(row.invoice_total),
            )
        )

    # 4) duplicates (same customer + period + total)
    dup_cols = ["customer_id", "period_start", "period_end", "invoice_total"]
    dups = invoices[invoices.duplicated(subset=dup_cols, keep=False)].sort_values(dup_cols)
    for row in dups.itertuples(index=False):
        discrepancies.append(
            Discrepancy(
                invoice_id=row.invoice_id,
                issue="POTENTIAL_DUPLICATE_INVOICE",
                expected=None,
                actual=float(row.invoice_total),
            )
        )

    return discrepancies
