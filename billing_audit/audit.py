from dataclasses import dataclass
import pandas as pd


@dataclass
class Discrpenancy:
    invoice_id: str
    issue: str
    expected: float | None
    actual: float | None


def audit(invoices: pd.DataFrame, line_items:pd.DataFrame,tol: float = 0.01) -> list[Discrpenancy]:
    discrepanices: list[Discrpenancy] = []

    li_sum = (
        line_items.groupby("invoice_id",as_index=False)[line_items]
        .sum()
        .rename(columns={"line_total":"line_items_total"})

    )