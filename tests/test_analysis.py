import tempfile
from pathlib import Path

import pandas as pd

from analysis import build_executive_summary, build_summary_report
from dashboard import (
    choose_category_chart,
    choose_distribution_chart,
    choose_trend_chart,
    get_dimension_summaries,
)
from data_loader import clean_data, load_and_clean
from visualization import plot_category_donut, plot_expense_distribution_pie


def test_build_executive_summary_contains_expected_sections():
    df = load_and_clean()
    report = build_executive_summary(df)

    assert report["kpis"]["total_revenue"] > 0
    assert not report["top_expense_categories"].empty
    assert not report["top_income_categories"].empty
    assert not report["region_summary"].empty
    assert not report["department_summary"].empty
    assert report["outlier_count"] >= 0


def test_build_summary_report_exposes_metrics():
    df = load_and_clean()
    summary = build_summary_report(df)

    assert list(summary.columns) == ["Metric", "Value"]
    assert "Total Revenue" in summary["Metric"].tolist()
    assert "Total Expenses" in summary["Metric"].tolist()


def test_clean_data_accepts_alias_columns_and_extra_columns():
    csv_text = """Transaction Date,Transaction Type,Department,Net Amount,Notes,Region
2026-01-01,Income,Sales,1200,Product sale,North
2026-01-02,Expense,Marketing,350,Ad spend,East
2026-01-03,Income,Operations,900,Service fee,West
"""

    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as fh:
        fh.write(csv_text)
        temp_path = fh.name

    try:
        df = clean_data(pd.read_csv(temp_path))
    finally:
        Path(temp_path).unlink(missing_ok=True)

    assert {"Date", "Type", "Category", "Amount", "Description"}.issubset(df.columns)
    assert len(df) == 3
    assert df["Type"].isin(["Income", "Expense"]).all()


def test_clean_data_adds_missing_region_and_department_columns():
    df = pd.DataFrame(
        {
            "Date": ["2026-01-01", "2026-01-02"],
            "Type": ["Income", "Expense"],
            "Category": ["Sales", "Marketing"],
            "Amount": [1000, 250],
            "Description": ["North office (Finance dept)", "South support"],
        }
    )

    cleaned = clean_data(df)

    assert "Region" in cleaned.columns
    assert "Department" in cleaned.columns
    assert cleaned["Region"].tolist() == ["North", "South"]
    assert cleaned["Department"].tolist() == ["Finance", "Unknown"]


def test_executive_summary_handles_missing_region_and_department_columns():
    df = load_and_clean().drop(columns=["Region", "Department"])

    report = build_executive_summary(df)

    assert not report["region_summary"].empty
    assert not report["department_summary"].empty


def test_dashboard_falls_back_to_dimension_summaries_when_keys_are_missing():
    df = load_and_clean()
    executive_summary = {"kpis": {}, "monthly_summary": pd.DataFrame()}

    region_summary, department_summary = get_dimension_summaries(executive_summary, df)

    assert not region_summary.empty
    assert not department_summary.empty


def test_dashboard_falls_back_when_analysis_helpers_are_missing(monkeypatch):
    df = load_and_clean()
    monkeypatch.delattr("analysis.region_summary", raising=False)
    monkeypatch.delattr("analysis.department_summary", raising=False)

    region_summary, department_summary = get_dimension_summaries({}, df)

    assert not region_summary.empty
    assert not department_summary.empty


def test_pie_charts_expose_legends_for_labelled_categories():
    category_df = pd.DataFrame(
        {
            "Category": ["Marketing", "Operations", "Travel", "Software", "Salaries"],
            "Total": [1200, 900, 400, 300, 250],
        }
    )

    pie_fig = plot_expense_distribution_pie(category_df)
    donut_fig = plot_category_donut(category_df)

    assert pie_fig.axes[0].legend_ is not None
    assert donut_fig.axes[0].legend_ is not None


def test_chart_selector_returns_expected_functions():
    assert choose_trend_chart("Line").__name__ == "plot_revenue_trend"
    assert choose_trend_chart("Bar").__name__ == "plot_revenue_vs_expense"
    assert choose_category_chart("Donut").__name__ == "plot_category_donut"
    assert choose_distribution_chart("Box Plot").__name__ == "plot_expense_boxplot"
