# Monthly Financial Analysis Dashboard

## Complete Setup and Usage Note

### 1. Project Overview

The **Monthly Financial Analysis Dashboard** is a Python-based financial analytics application that reads transaction data from a CSV file, cleans and validates the data, calculates important financial KPIs, and displays the results through an interactive Streamlit dashboard.

The project can analyze:

* Revenue
* Expenses
* Net Profit
* Savings Rate
* Monthly Growth
* Category-wise spending
* Region-wise performance
* Department-wise performance
* Expense outliers
* Transaction distributions

It also provides interactive charts and allows users to download a summary report.

---

## 2. Project Folder

The project is located at:

```text
C:\Users\dell\Downloads\Monthly_Financial_Analysis_Dashboard
```

The expected project structure is:

```text
Monthly_Financial_Analysis_Dashboard/
│
├── data/
│   └── financial_data.csv
│
├── reports/
│   └── summary_report.csv
│
├── tests/
│   └── test_analysis.py
│
├── config.py
├── data_loader.py
├── analysis.py
├── visualization.py
├── dashboard.py
├── generate_report.py
└── requirements.txt
```

### File Responsibilities

| File                      | Purpose                                                      |
| ------------------------- | ------------------------------------------------------------ |
| `config.py`               | Stores paths, colors, column names, and application settings |
| `data_loader.py`          | Loads, cleans, validates, and prepares CSV data              |
| `analysis.py`             | Calculates financial metrics and KPIs                        |
| `visualization.py`        | Creates charts and visualizations                            |
| `dashboard.py`            | Main Streamlit dashboard                                     |
| `generate_report.py`      | Generates the executive summary report                       |
| `tests/test_analysis.py`  | Automated tests                                              |
| `data/financial_data.csv` | Sample transaction dataset                                   |
| `reports/`                | Stores generated reports                                     |

---

# 3. Required CSV Data

The default dataset is:

```text
data\financial_data.csv
```

The expected columns are:

```text
Date
Type
Category
Amount
Description
```

Example:

| Date       | Type    | Category | Amount | Description       |
| ---------- | ------- | -------- | -----: | ----------------- |
| 2026-01-05 | Income  | Sales    |  50000 | Monthly sales     |
| 2026-01-08 | Expense | Salaries |  15000 | Employee salaries |
| 2026-01-12 | Expense | Travel   |   3000 | Business travel   |
| 2026-01-20 | Income  | Services |  25000 | Service income    |

The application can also recognize some alternate column names, such as:

* `Transaction Date` → `Date`
* `Net Amount` → `Amount`
* `Notes` → `Description`

The `Type` column should contain:

```text
Income
Expense
```

---

# 4. Open the Project in VS Code

1. Open **Visual Studio Code**.
2. Select:

```text
File → Open Folder
```

3. Select:

```text
C:\Users\dell\Downloads\Monthly_Financial_Analysis_Dashboard
```

4. Open the VS Code terminal:

```text
Terminal → New Terminal
```

The terminal should show something similar to:

```text
PS C:\Users\dell\Downloads\Monthly_Financial_Analysis_Dashboard>
```

This confirms that the terminal is working inside the project folder.

---

# 5. Create a Virtual Environment

Run:

```powershell
python -m venv venv
```

This creates a separate Python environment named:

```text
venv
```

The virtual environment keeps the project's packages separate from other Python projects on the computer.

---

# 6. Activate the Virtual Environment

For Windows PowerShell, run:

```powershell
venv\Scripts\activate
```

After successful activation, the terminal should look similar to:

```text
(venv) PS C:\Users\dell\Downloads\Monthly_Financial_Analysis_Dashboard>
```

The important part is:

```text
(venv)
```

---

# 7. Upgrade pip

Run:

```powershell
python -m pip install --upgrade pip
```

Wait until the command finishes successfully.

---

# 8. Install Required Packages

If `requirements.txt` exists, use:

```powershell
pip install -r requirements.txt
```

Alternatively, install the required packages directly:

```powershell
pip install streamlit pandas numpy matplotlib seaborn pytest
```

### Package Purpose

| Package    | Purpose                     |
| ---------- | --------------------------- |
| Streamlit  | Interactive dashboard       |
| Pandas     | Data loading and processing |
| NumPy      | Numerical calculations      |
| Matplotlib | Charts                      |
| Seaborn    | Advanced chart styling      |
| Pytest     | Automated testing           |

---

# 9. Verify the Sample Data

In the VS Code Explorer, confirm that this file exists:

```text
data\financial_data.csv
```

If the file is present, continue.

If it is missing, the dashboard may not be able to load the default sample data.

---

# 10. Run the Automated Tests

Before starting the dashboard, test the analysis functions.

Run:

```powershell
pytest tests\test_analysis.py -v
```

The tests should display results containing:

```text
PASSED
```

For example:

```text
test_analysis.py::test_revenue PASSED
test_analysis.py::test_expenses PASSED
test_analysis.py::test_profit PASSED
```

The exact test names may differ depending on the implementation.

### Important

If the tests fail, stop and fix the error before starting the dashboard.

Copy the complete error message if assistance is needed.

---

# 11. Start the Streamlit Dashboard

After the tests pass, run:

```powershell
streamlit run dashboard.py
```

Streamlit should display something similar to:

```text
Local URL: http://localhost:8501
```

Open the following address in your browser:

```text
http://localhost:8501
```

The dashboard should now be available.

---

# 12. Dashboard Features

The dashboard provides several filters in the sidebar.

### Filters

* Year
* Month
* Category
* Region
* Department

Changing these filters updates the financial analysis and charts.

---

# 13. Dashboard Tabs

## Tab 1 — Trends

The Trends section shows financial performance over time.

Available chart styles include:

* Line Chart
* Bar Chart
* Area Chart

This section can be used to identify increases or decreases in revenue and financial performance.

---

## Tab 2 — Category Breakdown

This section analyzes expenses or transactions by category.

Available chart styles include:

* Pie Chart
* Donut Chart
* Horizontal Bar Chart

Example categories:

* Salaries
* Travel
* Hardware
* Software
* Marketing
* Utilities

---

## Tab 3 — Distribution

This section analyzes the distribution of transaction amounts.

Available visualizations include:

* Heatmap
* Histogram
* Box Plot

The box plot can also help identify unusually large or small transactions.

---

## Tab 4 — Comparisons

This section compares different parts of the business.

It can include:

* Income vs. Expense scatter plots
* Region summaries
* Department summaries

This makes it easier to compare financial performance across different business areas.

---

# 14. Financial KPIs

The application calculates important financial metrics.

### Revenue

Total income:

```text
Revenue = Total Income
```

### Expenses

Total expenses:

```text
Expenses = Total Expense
```

### Net Profit

```text
Net Profit = Revenue - Expenses
```

### Savings Rate

A typical savings-rate calculation is:

```text
Savings Rate = (Net Profit / Revenue) × 100
```

### Growth Rate

Growth can be calculated by comparing the current period with the previous period.

```text
Growth Rate =
((Current Period - Previous Period) / Previous Period) × 100
```

The exact implementation should follow the formulas defined in `analysis.py`.

---

# 15. Data Cleaning

The data loader is responsible for preparing the raw CSV data.

It can handle issues such as:

* Missing values
* Invalid dates
* Invalid amounts
* Duplicate transactions
* Alternate column names
* Invalid transaction types

The dashboard can also display cleaning statistics so the user can understand how much data was removed or corrected.

---

# 16. Upload Your Own CSV

The dashboard includes a file-upload option.

You can upload your own financial CSV instead of using:

```text
data\financial_data.csv
```

Your CSV should contain the required information:

```text
Date
Type
Category
Amount
Description
```

The application may also recognize supported alternate column names.

The `Type` field should contain valid values such as:

```text
Income
Expense
```

---

# 17. Download the Summary

The dashboard provides a:

```text
Download Summary Report (CSV)
```

button.

This allows the currently filtered financial summary to be downloaded as a CSV file.

The generated summary can be used for further analysis in Excel or other data-analysis tools.

---

# 18. Generate the Executive Summary

The executive summary can be generated separately.

Open another terminal while the virtual environment is active.

Run:

```powershell
python generate_report.py
```

The report should be generated in:

```text
reports\executive_summary.md
```

The report provides a written summary of the financial results.

---

# 19. Complete Command Sequence

For a fresh setup, run these commands in order:

```powershell
cd "C:\Users\dell\Downloads\Monthly_Financial_Analysis_Dashboard"

python -m venv venv

venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt

pytest tests\test_analysis.py -v

streamlit run dashboard.py
```

If `requirements.txt` is not available, use:

```powershell
pip install streamlit pandas numpy matplotlib seaborn pytest
```

Then run:

```powershell
pytest tests\test_analysis.py -v
```

and finally:

```powershell
streamlit run dashboard.py
```

---

# 20. Optional Report Command

After activating the virtual environment:

```powershell
python generate_report.py
```

Expected output:

```text
reports\executive_summary.md
```

---

# 21. Troubleshooting

### Problem: `(venv)` does not appear

Run:

```powershell
venv\Scripts\activate
```

Make sure you are inside the project folder.

---

### Problem: `ModuleNotFoundError`

Make sure the virtual environment is active:

```text
(venv)
```

Then install the packages:

```powershell
pip install streamlit pandas numpy matplotlib seaborn pytest
```

---

### Problem: Tests fail

Run:

```powershell
pytest tests\test_analysis.py -v
```

Read the complete error message and fix the reported issue before starting Streamlit.

---

### Problem: Dashboard does not open automatically

Start the application:

```powershell
streamlit run dashboard.py
```

Then manually open:

```text
http://localhost:8501
```

---

### Problem: CSV column error

Check that the uploaded CSV contains:

```text
Date
Type
Category
Amount
Description
```

Also check that `Type` contains valid values such as:

```text
Income
Expense
```

---

# 22. Final Verification Checklist

* [ ] Project opened in VS Code
* [ ] Terminal is inside the project folder
* [ ] Virtual environment created
* [ ] Virtual environment activated
* [ ] `(venv)` appears in the terminal
* [ ] pip upgraded
* [ ] Required packages installed
* [ ] `data\financial_data.csv` exists
* [ ] Automated tests passed
* [ ] Streamlit dashboard started
* [ ] `http://localhost:8501` opens
* [ ] Sidebar filters work
* [ ] Trends charts work
* [ ] Category charts work
* [ ] Distribution charts work
* [ ] Comparison section works
* [ ] CSV download works
* [ ] Executive report generated, if required

---

# 23. Final Result

Once the setup is complete, the main command for using the application is:

```powershell
streamlit run dashboard.py
```

Then open:

```text
http://localhost:8501
```

The project provides a complete workflow:

```text
CSV Data
   ↓
Data Cleaning & Validation
   ↓
Financial Analysis
   ↓
KPI Calculation
   ↓
Interactive Streamlit Dashboard
   ↓
Charts & Comparisons
   ↓
CSV Summary / Executive Report
```

This gives you a modular, beginner-friendly financial analytics application where data loading, analysis, visualization, dashboard functionality, reporting, and testing are separated into their own components.
