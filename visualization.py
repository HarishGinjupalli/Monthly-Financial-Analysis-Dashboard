"""Chart functions for the finance dashboard."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import config

try:
    import seaborn as sns
    sns.set_theme(style="whitegrid")
    _HAS_SEABORN = True
except ImportError:
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "ggplot")
    _HAS_SEABORN = False


def _new_fig(figsize=config.FIGSIZE_WIDE):
    """
    Create a matplotlib Figure/Axes pair with the project's shared style.

    Why this function exists:
        Every chart function below needs the same figure setup
        (size, tight layout). Centralizing it keeps all charts
        visually consistent and avoids copy-pasted boilerplate.

    Args:
        figsize (tuple):
            (width, height) in inches.

    Returns:
        tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]
    """
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    return fig, ax


def _currency_axis(ax, axis="y"):
    """
    Format an axis's tick labels as currency ($1,200 instead of 1200).

    Args:
        ax (matplotlib.axes.Axes):
            The axis to format.
        axis (str):
            Either "y" or "x".
    """
    formatter = mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    if axis == "y":
        ax.yaxis.set_major_formatter(formatter)
    else:
        ax.xaxis.set_major_formatter(formatter)


def plot_revenue_trend(monthly_df: pd.DataFrame):
    """
    Line chart: Monthly Revenue Trend.

    Args:
        monthly_df (pandas.DataFrame):
            Output of analysis.monthly_summary().

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = _new_fig()
    ax.plot(monthly_df["Month"], monthly_df["Income"], marker="o",
            color=config.COLOR_INCOME, linewidth=2.5)
    ax.set_title("Monthly Revenue Trend", fontsize=13, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    _currency_axis(ax)
    fig.tight_layout()
    return fig


def plot_revenue_vs_expense(monthly_df: pd.DataFrame):
    """
    Bar chart: Revenue vs Expense, grouped by month.

    Args:
        monthly_df (pandas.DataFrame):
            Output of analysis.monthly_summary().

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = _new_fig()
    x = np.arange(len(monthly_df))
    width = 0.38
    ax.bar(x - width / 2, monthly_df["Income"], width, label="Revenue", color=config.COLOR_INCOME)
    ax.bar(x + width / 2, monthly_df["Expense"], width, label="Expense", color=config.COLOR_EXPENSE)
    ax.set_xticks(x)
    ax.set_xticklabels(monthly_df["Month"])
    ax.set_title("Revenue vs Expense by Month", fontsize=13, fontweight="bold")
    ax.set_ylabel("Amount")
    ax.legend()
    _currency_axis(ax)
    fig.tight_layout()
    return fig


def plot_expense_distribution_pie(category_df: pd.DataFrame):
    """
    Pie chart: Expense Distribution by category.

    Args:
        category_df (pandas.DataFrame):
            Output of analysis.category_summary(df, "Expense").

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = _new_fig((8, 7))
    labels = category_df["Category"].astype(str).tolist()
    values = category_df["Total"].astype(float).tolist()

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        colors=config.COLOR_PALETTE[: len(values)],
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1},
        pctdistance=0.6,
        labeldistance=1.1,
    )
    for text in texts:
        text.set_fontsize(9)
    for autotext in autotexts:
        autotext.set_fontsize(8)
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False)
    ax.set_title("Expense Distribution by Category", fontsize=13, fontweight="bold")
    ax.set_aspect("equal")
    fig.tight_layout()
    return fig


def plot_category_donut(category_df: pd.DataFrame, title: str = "Category Spending"):
    """
    Donut chart: Category Spending (pie chart with a hollow center).

    Args:
        category_df (pandas.DataFrame):
            Output of analysis.category_summary().
        title (str):
            Chart title.

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = _new_fig((8, 7))
    labels = category_df["Category"].astype(str).tolist()
    values = category_df["Total"].astype(float).tolist()

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        colors=config.COLOR_PALETTE[: len(values)],
        startangle=90,
        pctdistance=0.82,
        labeldistance=1.1,
        wedgeprops={"edgecolor": "white", "linewidth": 1},
    )
    for text in texts:
        text.set_fontsize(9)
    for autotext in autotexts:
        autotext.set_fontsize(8)
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    center_circle = plt.Circle((0, 0), 0.55, fc="white")
    fig.gca().add_artist(center_circle)
    ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_aspect("equal")
    fig.tight_layout()
    return fig


def plot_top_expense_categories(category_df: pd.DataFrame, top_n: int = config.TOP_N_CATEGORIES):
    """
    Horizontal bar chart: Top N Expense Categories.

    Args:
        category_df (pandas.DataFrame):
            Output of analysis.category_summary(df, "Expense").
        top_n (int):
            How many categories to show. Defaults to config.TOP_N_CATEGORIES.

    Returns:
        matplotlib.figure.Figure
    """
    top = category_df.head(top_n).sort_values("Total")  # ascending so the biggest bar ends up on top
    fig, ax = _new_fig((8, 5))
    ax.barh(top["Category"], top["Total"], color=config.COLOR_PALETTE[:len(top)])
    ax.set_title(f"Top {top_n} Expense Categories", fontsize=13, fontweight="bold")
    ax.set_xlabel("Total Amount")
    ax.invert_yaxis()
    _currency_axis(ax, axis="x")
    fig.tight_layout()
    return fig


def plot_cash_flow_area(monthly_df: pd.DataFrame):
    """
    Area chart: Monthly Cash Flow (cumulative net profit over time).

    Args:
        monthly_df (pandas.DataFrame):
            Output of analysis.monthly_summary().

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = _new_fig()
    cumulative = monthly_df["Profit"].cumsum()
    ax.fill_between(monthly_df["Month"], cumulative, color=config.COLOR_NET, alpha=0.35)
    ax.plot(monthly_df["Month"], cumulative, color=config.COLOR_NET, linewidth=2)
    ax.set_title("Monthly Cash Flow (Cumulative)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Cumulative Net Cash")
    _currency_axis(ax)
    fig.tight_layout()
    return fig


def plot_monthly_activity_heatmap(df: pd.DataFrame):
    """
    Heatmap: Monthly Financial Activity (Category x Month totals).

    Args:
        df (pandas.DataFrame):
            Cleaned transaction data (expenses only are used, since
            that's where category-level detail is meaningful).

    Returns:
        matplotlib.figure.Figure
    """
    expense_df = df[df[config.COL_TYPE] == config.EXPENSE_LABEL]
    pivot = pd.pivot_table(
        expense_df, index="Category", columns="Month", values=config.COL_AMOUNT,
        aggfunc="sum", fill_value=0.0,
    )
    # Reorder columns chronologically using the same helper analysis.py uses.
    from utils import month_sort_key
    pivot = pivot[sorted(pivot.columns, key=month_sort_key)]

    fig, ax = _new_fig((10, 6))
    if _HAS_SEABORN:
        sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax, cbar_kws={"label": "Amount"})
    else:
        im = ax.imshow(pivot.values, cmap="YlOrRd", aspect="auto")
        ax.set_xticks(range(len(pivot.columns)))
        ax.set_xticklabels(pivot.columns)
        ax.set_yticks(range(len(pivot.index)))
        ax.set_yticklabels(pivot.index)
        fig.colorbar(im, ax=ax, label="Amount")
    ax.set_title("Monthly Financial Activity by Category", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


def plot_transaction_histogram(df: pd.DataFrame):
    """
    Histogram: distribution of transaction amounts.

    Args:
        df (pandas.DataFrame):
            Cleaned transaction data.

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = _new_fig()
    ax.hist(df[config.COL_AMOUNT], bins=25, color=config.COLOR_PALETTE[1], edgecolor="white")
    ax.set_title("Transaction Amount Distribution", fontsize=13, fontweight="bold")
    ax.set_xlabel("Transaction Amount")
    ax.set_ylabel("Number of Transactions")
    _currency_axis(ax, axis="x")
    fig.tight_layout()
    return fig


def plot_expense_boxplot(df: pd.DataFrame):
    """
    Box plot: Expense Outliers by category.

    Args:
        df (pandas.DataFrame):
            Cleaned transaction data.

    Returns:
        matplotlib.figure.Figure
    """
    expense_df = df[df[config.COL_TYPE] == config.EXPENSE_LABEL]
    fig, ax = _new_fig((10, 5))
    if _HAS_SEABORN:
        sns.boxplot(data=expense_df, x="Category", y=config.COL_AMOUNT, ax=ax,
                    hue="Category", palette=config.COLOR_PALETTE, legend=False)
    else:
        categories = expense_df["Category"].unique()
        data = [expense_df.loc[expense_df["Category"] == c, config.COL_AMOUNT] for c in categories]
        ax.boxplot(data, labels=categories)
    ax.set_title("Expense Outliers by Category", fontsize=13, fontweight="bold")
    ax.set_ylabel("Amount")
    ax.tick_params(axis="x", rotation=35)
    _currency_axis(ax)
    fig.tight_layout()
    return fig


def plot_income_vs_expense_scatter(monthly_df: pd.DataFrame):
    """
    Scatter plot: Income vs Expense, one point per month.

    Args:
        monthly_df (pandas.DataFrame):
            Output of analysis.monthly_summary().

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = _new_fig(config.FIGSIZE_MEDIUM)
    ax.scatter(monthly_df["Expense"], monthly_df["Income"], s=120,
               color=config.COLOR_NET, edgecolor="white", linewidth=1.5, zorder=3)
    for _, row in monthly_df.iterrows():
        ax.annotate(row["Month"], (row["Expense"], row["Income"]),
                    textcoords="offset points", xytext=(6, 6), fontsize=8)
    ax.set_title("Income vs Expense by Month", fontsize=13, fontweight="bold")
    ax.set_xlabel("Expense")
    ax.set_ylabel("Income")
    _currency_axis(ax, axis="x")
    _currency_axis(ax, axis="y")
    fig.tight_layout()
    return fig
