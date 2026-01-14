# billing_validator

## Billing Audit Tool (Python)

### What it does

* Using two CSV files (invoices and line items), the tool:
* Compares invoice totals with summed line items
* Flags invoices with missing line items
* Detects negative invoice totals
* Identifies potential duplicate invoices
* Outputs results to **CSV** and **JSON**
* Prints a concise summary to the console

### Why I built this

I built this to practise Python in a realistic billing-systems context, focusing on:

* Investigating financial data discrepancies

* Automating manual support checks

* Producing machine- and human-readable reports

This reflects the kind of analysis typically performed in production support and business systems roles.

###  Requirements

* Python 3.9+
* Dependencies listed in requirements.txt

### Setup

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

### Running the tool in the terminal

python -m billing_audit.cli \
  --invoices data/sample_invoices.csv \
  --line-items data/sample_line_items.csv

Optional arguments:

--out-csv report.csv

--out-json report.json

--tolerance 0.01

### Example Output

Console:

Discrepancies found: 4
invoice_id  issue                      expected  actual
INV002      TOTAL_MISMATCH             200.0     190.0
INV003      POTENTIAL_DUPLICATE_INVOICE          200.0

Files:

* report.csv
* report.json

### Testing - run this in the terminal

pytest

