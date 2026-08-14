# 📊 Monthly Financial Analysis Dashboard

A Python-based financial analytics tool that reads transaction data, cleans it, calculates key financial metrics, and presents everything through an interactive Streamlit dashboard — plus a downloadable executive summary report.

---

## What It Does

- Reads transaction data from a CSV file (or a user-uploaded one)
- Cleans and validates the data (handles missing values, duplicates, flexible column names)
- Calculates core financial KPIs: revenue, expenses, net profit, savings rate, and growth rates
- Breaks results down by month, category, region, and department
- Detects statistical outliers in expenses
- Visualizes everything through interactive charts (trend lines, bar charts, pie/donut charts, heatmaps, box plots, scatter plots)
- Generates a written executive summary report (Markdown) and a downloadable CSV summary

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core logic |
| Pandas / NumPy | Data cleaning and analysis |
| Matplotlib / Seaborn | Charts |
| Streamlit | Interactive dashboard |
| Pytest | Automated tests |

---

## Project Structure

```
Monthly_Financial_Analysis_Dashboard/
│
├── data/
│   └── financial_data.csv        # Sample dataset
│
├── reports/
│   └── summary_report.csv        # Generated summary output
│
├── tests/
│   └── test_analysis.py          # Automated test suite
│
├── config.py                     # Paths, colors, column names, app settings
├── data_loader.py                # Loads and cleans the CSV
├── analysis.py                   # Calculates financial metrics and KPIs
├── visualization.py              # Builds all charts
├── dashboard.py                  # Streamlit web app (main entry point)
├── generate_report.py            # Creates the executive summary report
└── requirements.txt
```

Each file has a single, clear responsibility — open any of them and follow the flow from raw data → cleaning → analysis → charts.

---

## Expected CSV Columns

The app works with a CSV containing:

| Column | Description |
|---|---|
| `Date` | Transaction date |
| `Type` | `Income` or `Expense` |
| `Category` | e.g. Salaries, Travel, Hardware, Software |
| `Amount` | Transaction amount |
| `Description` | Free-text description |

The loader also recognizes common alternate column names (e.g. `Transaction Date`, `Net Amount`, `Notes`), so it can adapt to slightly different CSV formats without extra setup.

---

## Setup and Run

### 1. Open the project
Open the project folder in VS Code, then open a terminal inside it (**Terminal → New Terminal**). Confirm the prompt shows you're inside the project folder.

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate it
```bash
venv\Scripts\activate
```
You should see `(venv)` appear at the start of your terminal prompt.

### 4. Upgrade pip
```bash
python -m pip install --upgrade pip
```

### 5. Install dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` isn't present, install directly:
```bash
pip install streamlit pandas numpy matplotlib seaborn pytest
```

| Package | Role |
|---|---|
| `streamlit` | Dashboard UI |
| `pandas` | Data processing |
| `numpy` | Calculations |
| `matplotlib` | Charts |
| `seaborn` | Enhanced chart styling (optional — falls back gracefully if missing) |
| `pytest` | Automated tests |

### 6. Confirm the sample data exists
Check that `data/financial_data.csv` is present in the project folder — this is the bundled sample dataset used whenever you don't upload your own file.

### 7. Run the test suite
```bash
pytest tests/test_analysis.py -v
```
All tests should report `PASSED`. If anything fails, resolve it before moving on — the dashboard depends on the same functions being tested here.

### 8. Launch the dashboard
```bash
streamlit run dashboard.py
```
This opens your browser to **http://localhost:8501**. If it doesn't open automatically, visit that URL manually.

### 9. (Optional) Generate the executive summary report
In a separate terminal (with `venv` still active):
```bash
python generate_report.py
```
This writes a Markdown report to `reports/executive_summary.md`.

---

## Using the Dashboard

**Sidebar filters:**
- Year, Month, Category, Region, Department

**Chart tabs:**
1. **Trends** — revenue over time (Line / Bar / Area)
2. **Category Breakdown** — spending by category (Pie / Donut / Horizontal Bar)
3. **Distribution** — spread of transaction amounts (Heatmap / Histogram / Box Plot)
4. **Comparisons** — income vs. expense scatter plot, plus region and department summary tables

**Chart style switching:** each tab's chart type can be changed live from the sidebar.

**Upload your own data:** use the file uploader in the sidebar to analyze your own CSV instead of the bundled sample — no code changes required, as long as the required columns are present (or recognizable aliases).

**Export:** use the **Download Summary Report (CSV)** button to export the currently filtered KPI summary.

---

## Quick Command Reference

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest tests/test_analysis.py -v
streamlit run dashboard.py

# optional
python generate_report.py
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `(venv)` doesn't appear after activating | Make sure you're running the activate command from inside the project folder, and that you're using the Windows path syntax (`venv\Scripts\activate`) |
| `ModuleNotFoundError` | Confirm the virtual environment is active, then re-run `pip install -r requirements.txt` |
| Tests fail | Copy the full error message before continuing — don't proceed to the dashboard step until tests pass, since the dashboard relies on the same underlying functions |
| Dashboard won't open in browser | Manually visit `http://localhost:8501` |
| Uploaded CSV throws a column error | Check it includes `Date`, `Type`, `Category`, `Amount`, `Description` (or a recognized alias) and that `Type` contains only `Income`/`Expense` values |

---

## Notes

- The codebase is intentionally modular and beginner-friendly — each file has one clear job.
- Data cleaning statistics (rows dropped for invalid dates/amounts or duplicates) are surfaced in the dashboard sidebar for transparency.
- This project uses the bundled sample dataset (`data/financial_data.csv`) by default; no external API or database connection is required.
============================================================
MONTHLY FINANCIAL ANALYSIS DASHBOARD
COMPLETE SETUP GUIDE
============================================================

PROJECT FOLDER:
C:\Users\dell\Downloads\Monthly_Financial_Analysis_Dashboard


STEP 1 — OPEN THE PROJECT
-------------------------

1. Open VS Code.

2. Click:
   File → Open Folder

3. Select:
   C:\Users\dell\Downloads\Monthly_Financial_Analysis_Dashboard

4. Click "Select Folder".

5. Open the VS Code terminal:
   Terminal → New Terminal

6. Make sure the terminal is inside the project folder.

   It should look similar to:

   PS C:\Users\dell\Downloads\Monthly_Financial_Analysis_Dashboard>


============================================================
STEP 2 — CREATE A VIRTUAL ENVIRONMENT
============================================================

In the terminal, run:

python -m venv venv

Press Enter.

This creates a "venv" folder inside your project.


============================================================
STEP 3 — ACTIVATE THE VIRTUAL ENVIRONMENT
============================================================

Run:

venv\Scripts\activate

Press Enter.

You should now see "(venv)" at the beginning of your terminal.

Example:

(venv) PS C:\Users\dell\Downloads\Monthly_Financial_Analysis_Dashboard>


IMPORTANT:
If you see "(venv)", the virtual environment is active.


============================================================
STEP 4 — UPGRADE PIP
============================================================

Run:

python -m pip install --upgrade pip

Press Enter.

Wait until it finishes.


============================================================
STEP 5 — INSTALL REQUIRED PACKAGES
============================================================

Run:

pip install streamlit pandas numpy matplotlib seaborn pytest

Press Enter.

Wait until all packages finish installing.


The packages are:

streamlit  = Dashboard
pandas     = Data processing
numpy      = Calculations
matplotlib = Charts
seaborn    = Better charts
pytest     = Testing


============================================================
STEP 6 — CHECK THE DATA FILE
============================================================

In VS Code, look at the Explorer on the left.

You should have:

Monthly_Financial_Analysis_Dashboard
│
├── data
│   └── financial_data.csv
│
├── tests
│   └── test_analysis.py
│
├── analysis.py
├── dashboard.py
├── data_loader.py
├── visualization.py
└── generate_report.py


IMPORTANT:

This file must exist:

data\financial_data.csv

If you can see "financial_data.csv" inside the "data" folder,
continue to the next step.


============================================================
STEP 7 — RUN THE TESTS
============================================================

Make sure "(venv)" is still visible in the terminal.

Run:

pytest tests\test_analysis.py -v

Press Enter.

You should see:

PASSED

for the tests.

Example:

PASSED
PASSED
PASSED


IMPORTANT:

If all tests pass:
    Continue to Step 8.

If you get an ERROR:
    Stop here and copy the error message.
    Do not continue until the error is fixed.


============================================================
STEP 8 — START THE DASHBOARD
============================================================

Run:

streamlit run dashboard.py

Press Enter.

Streamlit should show something similar to:

Local URL: http://localhost:8501

Your browser may open automatically.

If it does not open automatically, open your browser and go to:

http://localhost:8501


============================================================
STEP 9 — USE THE DASHBOARD
============================================================

The dashboard should contain:

SIDEBAR FILTERS:
- Year
- Month
- Category
- Region
- Department


CHART TABS:
1. Trends
2. Category Breakdown
3. Distribution
4. Comparisons


Try changing the filters and check how the charts change.


============================================================
STEP 10 — UPLOAD YOUR OWN CSV (OPTIONAL)
============================================================

You can upload your own financial CSV file.

Your CSV should contain columns similar to:

Date
Type
Category
Amount
Description

The project also supports some flexible column-name aliases.


============================================================
STEP 11 — CHANGE CHART STYLES (OPTIONAL)
============================================================

You can change chart styles from the sidebar.

TREND CHARTS:
- Line
- Bar
- Area

CATEGORY CHARTS:
- Pie
- Donut
- Bar

DISTRIBUTION CHARTS:
- Heatmap
- Histogram
- Box Plot


============================================================
STEP 12 — GENERATE THE EXECUTIVE SUMMARY (OPTIONAL)
============================================================

If you want a written report:

1. Keep the dashboard running.

2. Open another VS Code terminal.

3. Make sure "(venv)" is active.

4. Run:

python generate_report.py

Press Enter.

The report should be created here:

reports\executive_summary.md


============================================================
QUICK COMMANDS — RUN IN THIS ORDER
============================================================

COMMAND 1:

python -m venv venv


COMMAND 2:

venv\Scripts\activate


COMMAND 3:

python -m pip install --upgrade pip


COMMAND 4:

pip install streamlit pandas numpy matplotlib seaborn pytest


COMMAND 5:

pytest tests\test_analysis.py -v


COMMAND 6:

streamlit run dashboard.py


OPTIONAL COMMAND:

python generate_report.py


============================================================
IF SOMETHING GOES WRONG
============================================================

If you get an error:

1. Do not delete the project.
2. Do not create another project.
3. Copy the complete error from the terminal.
4. Send the error to me.

I can tell you exactly which command to run to fix it.


============================================================
FINAL CHECK
============================================================

[ ] Project opened in VS Code
[ ] Terminal is inside the project folder
[ ] Virtual environment created
[ ] Virtual environment activated
[ ] "(venv)" appears in terminal
[ ] pip upgraded
[ ] Required packages installed
[ ] data\financial_data.csv exists
[ ] Tests passed
[ ] Dashboard started
[ ] http://localhost:8501 opens
[ ] Dashboard filters work
[ ] Charts work
[ ] Executive report generated (optional)


============================================================
DONE!
============================================================

Your dashboard is ready when:

streamlit run dashboard.py

starts successfully and you can open:

http://localhost:8501