"""Streamlit dashboard for the finance analysis project."""

import streamlit as st
import pandas as pd
import config
import data_loader
import analysis
import visualization as viz
from utils import format_currency, format_percent


def choose_trend_chart(chart_type: str):
    chart_map = {
        "Line": viz.plot_revenue_trend,
        "Bar": viz.plot_revenue_vs_expense,
        "Area": viz.plot_cash_flow_area,
    }
    return chart_map.get(chart_type, viz.plot_revenue_trend)


def choose_category_chart(chart_type: str):
    chart_map = {
        "Pie": viz.plot_expense_distribution_pie,
        "Donut": viz.plot_category_donut,
        "Horizontal Bar": viz.plot_top_expense_categories,
    }
    return chart_map.get(chart_type, viz.plot_expense_distribution_pie)


def choose_distribution_chart(chart_type: str):
    chart_map = {
        "Heatmap": viz.plot_monthly_activity_heatmap,
        "Histogram": viz.plot_transaction_histogram,
        "Box Plot": viz.plot_expense_boxplot,
    }
    return chart_map.get(chart_type, viz.plot_monthly_activity_heatmap)


def configure_page():
    """
    Set Streamlit page-level settings (title, icon, layout).

    Why this function exists:
        st.set_page_config() must be the very first Streamlit
        command that runs, so it's pulled into its own function
        and called at the top of main() for clarity.
    """
    st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON,
                        layout=config.PAGE_LAYOUT)


@st.cache_data(show_spinner=False)
def get_cleaned_data(file_bytes: bytes = None) -> pd.DataFrame:
    """
    Load and clean data, from an uploaded file if provided, else the default CSV.

    Why this function exists:
        Streamlit re-runs the whole script on every user interaction
        (e.g. changing a filter). @st.cache_data means the CSV is only
        re-read and re-cleaned when the underlying file actually
        changes, keeping the dashboard responsive.

    Args:
        file_bytes (bytes, optional):
            Raw bytes of an uploaded CSV file. If None, the bundled
            sample dataset (config.DEFAULT_DATA_FILE) is used instead.

    Returns:
        pandas.DataFrame:
            Cleaned, analysis-ready transaction data.
    """
    if file_bytes is not None:
        import io
        raw_df = pd.read_csv(io.BytesIO(file_bytes))
        missing = data_loader.validate_columns(raw_df)
        if missing:
            raise ValueError(f"Uploaded CSV is missing column(s): {', '.join(missing)}")
        return data_loader.clean_data(raw_df)
    return data_loader.load_and_clean()


def render_sidebar(df: pd.DataFrame):
    """
    Render the sidebar controls (CSV upload + Month/Year/Category filters).

    Args:
        df (pandas.DataFrame):
            The full cleaned dataset, used to populate filter options.

    Returns:
        tuple:
            (uploaded_file, selected_years, selected_months, selected_categories)
    """
    st.sidebar.header("\U0001F4C1 Data")
    uploaded_file = st.sidebar.file_uploader("Upload your own CSV", type=["csv"])
    st.sidebar.caption(
        f"Expected columns: {', '.join(config.REQUIRED_COLUMNS)}"
    )

    st.sidebar.header("\U0001F50D Filters")
    years = sorted(df["Year"].unique().tolist())
    selected_years = st.sidebar.multiselect("Year", years, default=years)

    months = sorted(df["Month"].unique().tolist(), key=lambda m: df.loc[df["Month"] == m, "MonthSortKey"].iloc[0])
    selected_months = st.sidebar.multiselect("Month", months, default=months)

    categories = sorted(df["Category"].unique().tolist())
    selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

    normalized = _ensure_dimension_columns(df)
    regions = sorted(normalized["Region"].astype(str).unique().tolist())
    selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

    departments = sorted(normalized["Department"].astype(str).unique().tolist())
    selected_departments = st.sidebar.multiselect("Department", departments, default=departments)

    st.sidebar.header("📈 Chart Style")
    trend_chart = st.sidebar.selectbox("Trend chart", ["Line", "Bar", "Area"], index=0)
    category_chart = st.sidebar.selectbox("Category chart", ["Pie", "Donut", "Horizontal Bar"], index=0)
    distribution_chart = st.sidebar.selectbox("Distribution chart", ["Heatmap", "Histogram", "Box Plot"], index=0)

    return uploaded_file, selected_years, selected_months, selected_categories, selected_regions, selected_departments, trend_chart, category_chart, distribution_chart


def _ensure_dimension_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure the business-dimension columns exist for filtering and display."""
    normalized = df.copy()
    if "Region" not in normalized.columns:
        normalized["Region"] = "Unknown"
    if "Department" not in normalized.columns:
        normalized["Department"] = "Unknown"
    return normalized


def apply_filters(df: pd.DataFrame, years, months, categories, regions, departments) -> pd.DataFrame:
    """
    Filter the dataset based on sidebar selections.

    Args:
        df (pandas.DataFrame):
            Full cleaned dataset.
        years (list):
            Selected years to keep.
        months (list):
            Selected month labels to keep.
        categories (list):
            Selected categories to keep.

    Returns:
        pandas.DataFrame:
            Filtered subset of the data.
    """
    normalized = _ensure_dimension_columns(df)
    filtered = normalized[
        normalized["Year"].isin(years)
        & normalized["Month"].isin(months)
        & normalized["Category"].isin(categories)
        & normalized["Region"].isin(regions)
        & normalized["Department"].isin(departments)
    ]
    return filtered


def render_kpi_cards(df: pd.DataFrame):
    """
    Render the row of KPI metric cards at the top of the dashboard.

    Args:
        df (pandas.DataFrame):
            Filtered transaction data.
    """
    kpis = analysis.calculate_kpis(df)

    row1 = st.columns(4)
    row1[0].metric("Total Revenue", format_currency(kpis["total_revenue"]))
    row1[1].metric("Total Expenses", format_currency(kpis["total_expenses"]))
    row1[2].metric("Net Profit", format_currency(kpis["net_profit"]))
    row1[3].metric("Savings Rate", format_percent(kpis["savings_rate"]))

    row2 = st.columns(4)
    row2[0].metric("Transactions", f"{kpis['transaction_count']:,}")
    row2[1].metric("Highest Expense", format_currency(kpis["highest_expense"]))
    row2[2].metric("Highest Income", format_currency(kpis["highest_income"]))
    row2[3].metric("Avg Monthly Spending", format_currency(kpis["avg_monthly_spending"]))


def _summarize_dimension(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Build a simple totals summary for a business dimension."""
    normalized = df.copy()
    if column_name not in normalized.columns:
        normalized[column_name] = "Unknown"

    grouped = normalized.groupby(column_name, as_index=False)[config.COL_AMOUNT].sum()
    grouped = grouped.rename(columns={config.COL_AMOUNT: "Total"})
    grouped = grouped.sort_values("Total", ascending=False).reset_index(drop=True)
    return grouped


def get_dimension_summaries(executive_summary: dict, df: pd.DataFrame):
    """Return region and department summaries, falling back safely if needed."""
    if executive_summary is None:
        executive_summary = {}

    region_summary = executive_summary.get("region_summary")
    department_summary = executive_summary.get("department_summary")

    region_helper = getattr(analysis, "region_summary", None)
    department_helper = getattr(analysis, "department_summary", None)

    if region_summary is None:
        if callable(region_helper):
            region_summary = region_helper(df)
        else:
            region_summary = _summarize_dimension(df, "Region")
    if department_summary is None:
        if callable(department_helper):
            department_summary = department_helper(df)
        else:
            department_summary = _summarize_dimension(df, "Department")

    return region_summary, department_summary


def render_charts(df: pd.DataFrame, trend_chart: str, category_chart: str, distribution_chart: str):
    """
    Render every chart, organized into tabs so the dashboard stays
    readable instead of showing ten charts in one long scroll.

    Args:
        df (pandas.DataFrame):
            Filtered transaction data.
    """
    monthly = analysis.monthly_summary(df)
    expense_cat = analysis.category_summary(df, config.EXPENSE_LABEL)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["\U0001F4C8 Trends", "\U0001F967 Category Breakdown", "\U0001F4CA Distribution", "\u2696\uFE0F Comparisons"]
    )

    with tab1:
        trend_func = choose_trend_chart(trend_chart)
        if trend_chart == "Line":
            st.pyplot(trend_func(monthly))
        elif trend_chart == "Bar":
            st.pyplot(trend_func(monthly))
        else:
            st.pyplot(trend_func(monthly))

    with tab2:
        category_func = choose_category_chart(category_chart)
        st.pyplot(category_func(expense_cat))

    with tab3:
        distribution_func = choose_distribution_chart(distribution_chart)
        st.pyplot(distribution_func(df))

    with tab4:
        st.pyplot(viz.plot_income_vs_expense_scatter(monthly))
        st.subheader("Regional and Department Analysis")
        executive_summary = analysis.build_executive_summary(df)
        region_summary, department_summary = get_dimension_summaries(executive_summary, df)
        col1, col2 = st.columns(2)
        with col1:
            st.write("Top Regions")
            st.dataframe(region_summary, use_container_width=True)
        with col2:
            st.write("Top Departments")
            st.dataframe(department_summary, use_container_width=True)
        st.subheader("Monthly Summary Table")
        st.dataframe(monthly.style.format({
            "Income": "${:,.0f}", "Expense": "${:,.0f}", "Profit": "${:,.0f}",
            "Revenue_Growth": "{:+.1%}", "Expense_Growth": "{:+.1%}",
        }), use_container_width=True)


def render_data_quality_note(df: pd.DataFrame):
    """
    Show a small transparency note about what the cleaning step removed.

    Args:
        df (pandas.DataFrame):
            The cleaned dataset (its .attrs dict carries cleaning stats,
            set in data_loader.clean_data()).
    """
    dropped_invalid = df.attrs.get("rows_dropped_invalid", 0)
    dropped_dupes = df.attrs.get("rows_dropped_duplicate", 0)
    if dropped_invalid or dropped_dupes:
        st.sidebar.info(
            f"Data cleaning removed {dropped_invalid} row(s) with an invalid "
            f"date/amount and {dropped_dupes} duplicate row(s)."
        )


def main():
    """
    Application entry point: wires the sidebar, KPIs, and charts together.
    """
    configure_page()
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    st.caption("Upload your own transaction CSV, or explore the bundled sample dataset.")

    # ------------------------------------------------------------
    # Load data first with defaults, so the sidebar filter widgets
    # have real Year/Month/Category options to populate from even
    # before a file is uploaded.
    # ------------------------------------------------------------
    try:
        base_df = data_loader.load_and_clean()
    except (FileNotFoundError, ValueError) as e:
        st.error(f"Could not load the sample dataset: {e}")
        st.stop()

    uploaded_file, sel_years, sel_months, sel_categories, sel_regions, sel_departments, trend_chart, category_chart, distribution_chart = render_sidebar(base_df)

    # ------------------------------------------------------------
    # If the user uploaded their own file, re-load using that instead.
    # Wrapped in try/except so a malformed upload shows a friendly
    # message instead of crashing the whole app.
    # ------------------------------------------------------------
    if uploaded_file is not None:
        try:
            df = get_cleaned_data(uploaded_file.getvalue())
        except (ValueError, pd.errors.ParserError) as e:
            st.error(f"There was a problem reading your file: {e}")
            st.stop()
    else:
        df = base_df

    render_data_quality_note(df)

    filtered_df = apply_filters(df, sel_years, sel_months, sel_categories, sel_regions, sel_departments)
    if filtered_df.empty:
        st.warning("No transactions match the current filters. Adjust the sidebar selections.")
        st.stop()

    render_kpi_cards(filtered_df)

    executive_summary = analysis.build_executive_summary(filtered_df)
    with st.expander("Executive Snapshot", expanded=True):
        st.write(
            f"Net profit is **{format_currency(executive_summary['kpis']['net_profit'])}** with a **{format_percent(executive_summary['kpis']['profit_margin'])}** margin."
        )
        st.write(
            f"The strongest month was **{executive_summary['best_month']['month']}** and the weakest was **{executive_summary['worst_month']['month']}**."
        )
        st.write(
            f"{executive_summary['outlier_count']} expense outlier(s) were detected for further review."
        )

    st.divider()
    render_charts(filtered_df, trend_chart, category_chart, distribution_chart)

    # ------------------------------------------------------------
    # Let the user export the current summary as a CSV report,
    # matching reports/summary_report.csv that ships with the project.
    # ------------------------------------------------------------
    st.divider()
    summary = analysis.build_summary_report(filtered_df)
    st.download_button(
        "\U0001F4E5 Download Summary Report (CSV)",
        data=summary.to_csv(index=False).encode("utf-8"),
        file_name="summary_report.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
