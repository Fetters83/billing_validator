import pandas as pd
from billing_audit.audit import audit

def test_flags_total_mismatch():
    invoices = pd.DataFrame([{"invoice_id":"INV1","customer_id":"C1","period_start":"2025-12-01","period_end":"2025-12-31","currency":"GBP","invoice_total":100.0}])
    line_items = pd.DataFrame([{"invoice_id":"INV1","sku":"A","qty":1,"unit_price":90.0,"tax":0.0,"discount":0.0,"line_total":90.0}])

    d = audit(invoices, line_items, tol=0.01)
    assert any(x.issue == "TOTAL_MISMATCH" for x in d)
