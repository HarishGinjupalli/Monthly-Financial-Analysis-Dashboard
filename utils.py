"""Small helper functions used across the project."""

from typing import Optional


def format_currency(value: float, symbol: str = "$") -> str:
    """Format a number as currency."""
    try:
        if value < 0:
            return f"({symbol}{abs(value):,.2f})"
        return f"{symbol}{value:,.2f}"
    except (TypeError, ValueError):
        return f"{symbol}0.00"


def format_percent(value: float, decimals: int = 1) -> str:
    """Format a decimal as a percentage."""
    try:
        return f"{value * 100:.{decimals}f}%"
    except (TypeError, ValueError):
        return "0.0%"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divide safely without crashing if the denominator is zero."""
    if denominator in (0, None) or (isinstance(denominator, float) and denominator == 0.0):
        return default
    return numerator / denominator


def calculate_growth_rate(current: float, previous: float) -> Optional[float]:
    """Calculate percentage growth between two values."""
    if previous in (0, None):
        return None
    return (current - previous) / previous


def month_sort_key(month_label: str) -> str:
    """Convert a month label like Jan-2026 into a sortable string."""
    months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    try:
        mon, year = month_label.split("-")
        return f"{year}-{months.get(mon, '99')}"
    except (ValueError, AttributeError):
        return "9999-99"
