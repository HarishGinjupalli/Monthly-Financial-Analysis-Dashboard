"""
Project:
Monthly Financial Analysis Dashboard

File:
config.py

Author:
Student Project

Version:
1.0

Purpose:
Central place for every constant used across the project: file paths,
color palettes, chart settings, and column names. Keeping these in one
file means changing a color or a path never requires touching the
logic in other modules.

Created:
2026-08-01
"""

# Simple usage (beginner-friendly):
# - This file only holds constants. Use them from other modules.
# Example:
# from config import DEFAULT_DATA_FILE, COLOR_INCOME
# print(DEFAULT_DATA_FILE)  # path to the bundled CSV
# print(COLOR_INCOME)       # color hex used for income charts


import os

# ----------------------------------------------------------------------
# FOLDER / FILE PATHS
# ----------------------------------------------------------------------
# BASE_DIR points to the folder this file lives in, so the project
# still works no matter where it is copied or run from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

DEFAULT_DATA_FILE = os.path.join(DATA_DIR, "financial_data.csv")
SUMMARY_REPORT_FILE = os.path.join(REPORTS_DIR, "summary_report.csv")

# ----------------------------------------------------------------------
# EXPECTED CSV COLUMNS
# ----------------------------------------------------------------------
# analysis.py and data_loader.py both rely on these exact names.
# If your own CSV uses different headers, rename them here once
# instead of hunting through every file.
COL_DATE = "Date"
COL_TYPE = "Type"          # expected values: "Income" or "Expense"
COL_CATEGORY = "Category"
COL_AMOUNT = "Amount"
COL_DESCRIPTION = "Description"

REQUIRED_COLUMNS = [COL_DATE, COL_TYPE, COL_CATEGORY, COL_AMOUNT, COL_DESCRIPTION]

INCOME_LABEL = "Income"
EXPENSE_LABEL = "Expense"

# ----------------------------------------------------------------------
# APP / UI SETTINGS
# ----------------------------------------------------------------------
APP_TITLE = "Monthly Financial Analysis Dashboard"
APP_ICON = "\U0001F4CA"  # bar chart emoji, shown in the browser tab
PAGE_LAYOUT = "wide"

# ----------------------------------------------------------------------
# CHART COLOR PALETTE
# ----------------------------------------------------------------------
# A single consistent palette so every chart in visualization.py
# looks like it belongs to the same dashboard.
COLOR_INCOME = "#2E7D32"     # green
COLOR_EXPENSE = "#C62828"    # red
COLOR_NET = "#1F3864"        # navy
COLOR_PALETTE = ["#1F3864", "#2E5395", "#8FAADC", "#F4B183", "#C55A11",
                  "#548235", "#A9D18E", "#BF9000", "#7030A0", "#C00000"]

# Figure size defaults keep every chart a consistent shape in the dashboard.
FIGSIZE_WIDE = (10, 4.5)
FIGSIZE_SQUARE = (6, 6)
FIGSIZE_MEDIUM = (7, 5)

# Number of top categories to show in "Top Expense Categories" chart.
TOP_N_CATEGORIES = 8
