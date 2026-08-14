"""Simple financial calculations used by the dashboard."""

import pandas as pd
import config
from utils import safe_divide, month_sort_key


def split_income_expense(df: pd.DataFrame):
    """
    Split a cleaned DataFrame into separate income and expense DataFrames.

    Why this function exists:
        Almost every calculation below needs "just the income rows"
        or "just the expense rows". Splitting once avoids repeating
        the same boolean filter in every function.

    Args:
        df (pandas.DataFrame):
            Cleaned transaction data (output of data_loader.clean_data).

    Returns:
        tuple[pandas.DataFrame, pandas.DataFrame]:
            (income_df, expense_df)
    """
    income_df = df[df[config.COL_TYPE] == config.INCOME_LABEL]
    expense_df = df[df[config.COL_TYPE] == config.EXPENSE_LABEL]
    return income_df, expense_df


def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate the headline KPI numbers shown on the dashboard's KPI cards.

    Args:
        df (pandas.DataFrame):
            Cleaned transaction data, optionally already filtered by
            the sidebar's month/year/category selections.

    Returns:
        dict:
            Keys: total_revenue, total_expenses, net_profit, savings_rate,
            transaction_count, highest_expense, highest_income,
            profit_margin, avg_daily_spending, avg_monthly_spending.
    """
    income_df, expense_df = split_income_expense(df)

    total_revenue = income_df[config.COL_AMOUNT].sum()
    total_expenses = expense_df[config.COL_AMOUNT].sum()
    net_profit = total_revenue - total_expenses

    # Savings rate: how much of revenue is left over after expenses.
    savings_rate = safe_divide(net_profit, total_revenue)
    # Profit margin is the same ratio in this dataset shape, kept as
    # a separate key because in a business context the two terms are
    # asked for separately in KPI requirements.
    profit_margin = savings_rate

    highest_expense = expense_df[config.COL_AMOUNT].max() if not expense_df.empty else 0.0
    highest_income = income_df[config.COL_AMOUNT].max() if not income_df.empty else 0.0

    # Average daily spending: total expenses spread over the number of
    # distinct calendar days covered by the (filtered) data.
    n_days = df[config.COL_DATE].dt.normalize().nunique() or 1
    avg_daily_spending = safe_divide(total_expenses, n_days)

    # Average monthly spending: total expenses spread over the number
    # of distinct months covered by the (filtered) data.
    n_months = df["Month"].nunique() or 1
    avg_monthly_spending = safe_divide(total_expenses, n_months)

    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "savings_rate": savings_rate,
        "profit_margin": profit_margin,
        "transaction_count": len(df),
        "highest_expense": highest_expense,
        "highest_income": highest_income,
        "avg_daily_spending": avg_daily_spending,
        "avg_monthly_spending": avg_monthly_spending,
    }


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a month-by-month table of income, expense, and profit.

    This is the SQL/Excel equivalent of a SUMIFS-by-month pivot: for
    every calendar month present in the data, total up income and
    expenses separately, then derive profit and growth rates.

    Args:
        df (pandas.DataFrame):
            Cleaned transaction data.

    Returns:
        pandas.DataFrame:
            Columns: Month, Income, Expense, Profit, Revenue_Growth,
            Expense_Growth -- one row per month, sorted chronologically.
    """
    # pivot_table is pandas' equivalent of an Excel PivotTable / SUMIFS:
    # it groups by Month and Type at once and sums Amount into each cell.
    pivot = pd.pivot_table(
        df, index="Month", columns=config.COL_TYPE, values=config.COL_AMOUNT,
        aggfunc="sum", fill_value=0.0,
    ).reset_index()

    for col in (config.INCOME_LABEL, config.EXPENSE_LABEL):
        if col not in pivot.columns:
            pivot[col] = 0.0

    pivot = pivot.rename(columns={config.INCOME_LABEL: "Income", config.EXPENSE_LABEL: "Expense"})
    pivot["Profit"] = pivot["Income"] - pivot["Expense"]

    # Sort chronologically (not alphabetically) using the helper from utils.py.
    pivot["_sort"] = pivot["Month"].apply(month_sort_key)
    pivot = pivot.sort_values("_sort").drop(columns="_sort").reset_index(drop=True)

    # Growth rates compare each month to the month before it.
    pivot["Revenue_Growth"] = pivot["Income"].pct_change()
    pivot["Expense_Growth"] = pivot["Expense"].pct_change()

    return pivot[["Month", "Income", "Expense", "Profit", "Revenue_Growth", "Expense_Growth"]]


def category_summary(df: pd.DataFrame, txn_type: str = config.EXPENSE_LABEL) -> pd.DataFrame:
    """
    Total transactions by category (SUMIF-by-category equivalent).

    Args:
        df (pandas.DataFrame):
            Cleaned transaction data.
        txn_type (str):
            Either config.EXPENSE_LABEL or config.INCOME_LABEL.

    Returns:
        pandas.DataFrame:
            Columns: Category, Total, Pct_Of_Total -- sorted descending
            by Total.
    """
    subset = df[df[config.COL_TYPE] == txn_type]
    grouped = subset.groupby("Category", as_index=False)[config.COL_AMOUNT].sum()
    grouped = grouped.rename(columns={config.COL_AMOUNT: "Total"})
    grouped = grouped.sort_values("Total", ascending=False).reset_index(drop=True)
    total_all = grouped["Total"].sum()
    grouped["Pct_Of_Total"] = grouped["Total"].apply(lambda x: safe_divide(x, total_all))
    return grouped


def budget_status(actual: float, budget: float) -> str:
    """
    Classify actual spending against a budget (IF()-formula equivalent).

    Args:
        actual (float):
            Actual amount spent.
        budget (float):
            Budgeted amount.

    Returns:
        str:
            "Over Budget", "Under Budget", or "On Budget".
    """
    # np.where / if-else here is the direct Python equivalent of the
    # Excel formula =IF(Actual>Budget,"Over Budget","Within Budget").
    if actual > budget:
        return "Over Budget"
    elif actual < budget:
        return "Under Budget"
    return "On Budget"


def _ensure_dimension_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure business-dimension columns exist even when the source data lacks them."""
    normalized = df.copy()
    if "Region" not in normalized.columns:
        normalized["Region"] = "Unknown"
    if "Department" not in normalized.columns:
        normalized["Department"] = "Unknown"
    return normalized


def region_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize spending and revenue by region."""
    normalized = _ensure_dimension_columns(df)
    grouped = normalized.groupby("Region", as_index=False)[config.COL_AMOUNT].sum()
    grouped = grouped.rename(columns={config.COL_AMOUNT: "Total"})
    grouped = grouped.sort_values("Total", ascending=False).reset_index(drop=True)
    return grouped


def department_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize spending and revenue by department."""
    normalized = _ensure_dimension_columns(df)
    grouped = normalized.groupby("Department", as_index=False)[config.COL_AMOUNT].sum()
    grouped = grouped.rename(columns={config.COL_AMOUNT: "Total"})
    grouped = grouped.sort_values("Total", ascending=False).reset_index(drop=True)
    return grouped


def detect_expense_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag expense transactions that are statistical outliers.

    Uses the standard IQR (interquartile range) method -- the same
    rule a box plot draws its whiskers from -- so the flagged rows
    line up with what the Box Plot chart visually highlights.

    Args:
        df (pandas.DataFrame):
            Cleaned transaction data.

    Returns:
        pandas.DataFrame:
            The subset of expense rows whose Amount falls outside
            1.5 * IQR from the first/third quartile.
    """
    _, expense_df = split_income_expense(df)
    if expense_df.empty:
        return expense_df

    q1 = expense_df[config.COL_AMOUNT].quantile(0.25)
    q3 = expense_df[config.COL_AMOUNT].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return expense_df[(expense_df[config.COL_AMOUNT] < lower) | (expense_df[config.COL_AMOUNT] > upper)]


def build_summary_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the flat summary table saved to reports/summary_report.csv.

    Args:
        df (pandas.DataFrame):
            Cleaned transaction data.

    Returns:
        pandas.DataFrame:
            One row per KPI, with a Metric and Value column -- a
            simple, spreadsheet-friendly export format.
    """
    kpis = calculate_kpis(df)
    rows = [
        ("Total Revenue", kpis["total_revenue"]),
        ("Total Expenses", kpis["total_expenses"]),
        ("Net Profit", kpis["net_profit"]),
        ("Savings Rate", kpis["savings_rate"]),
        ("Profit Margin", kpis["profit_margin"]),
        ("Number of Transactions", kpis["transaction_count"]),
        ("Highest Expense", kpis["highest_expense"]),
        ("Highest Income", kpis["highest_income"]),
        ("Average Daily Spending", kpis["avg_daily_spending"]),
        ("Average Monthly Spending", kpis["avg_monthly_spending"]),
    ]
    return pd.DataFrame(rows, columns=["Metric", "Value"])


def build_executive_summary(df: pd.DataFrame) -> dict:
    """
    Create a management-ready summary dictionary for executive reporting.

    This gathers KPI values, monthly trend context, top spending categories,
    and anomaly signals in a single structure that can be used by the
    dashboard, CLI report generator, and downstream export tools.
    """
    kpis = calculate_kpis(df)
    monthly = monthly_summary(df)
    expense_categories = category_summary(df, config.EXPENSE_LABEL).head(5)
    income_categories = category_summary(df, config.INCOME_LABEL).head(5)
    outliers = detect_expense_outliers(df)

    best_month = monthly.loc[monthly["Profit"].idxmax()]
    worst_month = monthly.loc[monthly["Profit"].idxmin()]

    return {
        "kpis": kpis,
        "monthly_summary": monthly,
        "top_expense_categories": expense_categories,
        "top_income_categories": income_categories,
        "region_summary": region_summary(df),
        "department_summary": department_summary(df),
        "outlier_count": len(outliers),
        "best_month": {
            "month": best_month["Month"],
            "profit": float(best_month["Profit"]),
        },
        "worst_month": {
            "month": worst_month["Month"],
            "profit": float(worst_month["Profit"]),
        },
    }


def build_executive_report_markdown(summary: dict) -> str:
    """Render a simple markdown executive summary for export and reporting."""
    kpis = summary["kpis"]
    expense_top = summary["top_expense_categories"]
    income_top = summary["top_income_categories"]

    lines = [
        "# Executive Financial Summary",
        "",
        "## KPI Snapshot",
        f"- Total Revenue: {kpis['total_revenue']:.2f}",
        f"- Total Expenses: {kpis['total_expenses']:.2f}",
        f"- Net Profit: {kpis['net_profit']:.2f}",
        f"- Profit Margin: {kpis['profit_margin']:.2%}",
        f"- Transaction Count: {kpis['transaction_count']}",
        f"- Expense Outliers Detected: {summary['outlier_count']}",
        "",
        "## Best and Worst Months",
        f"- Best Month: {summary['best_month']['month']} ({summary['best_month']['profit']:.2f})",
        f"- Worst Month: {summary['worst_month']['month']} ({summary['worst_month']['profit']:.2f})",
        "",
        "## Top Expense Categories",
    ]

    for _, row in expense_top.iterrows():
        lines.append(f"- {row['Category']}: {row['Total']:.2f} ({row['Pct_Of_Total']:.1%})")

    lines.extend(["", "## Top Income Categories"])
    for _, row in income_top.iterrows():
        lines.append(f"- {row['Category']}: {row['Total']:.2f} ({row['Pct_Of_Total']:.1%})")

    return "\n".join(lines) + "\n"
