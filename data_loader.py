"""Simple loading and cleaning helpers for the finance dashboard."""

import os
import re
import pandas as pd
import config


COLUMN_ALIASES = {
    config.COL_DATE: ["Date", "Transaction Date", "Txn Date", "Posting Date", "date"],
    config.COL_TYPE: ["Type", "Transaction Type", "Entry Type", "Nature", "Flow", "type"],
    config.COL_CATEGORY: ["Category", "Account", "Subcategory", "Department", "Segment", "category"],
    config.COL_AMOUNT: ["Amount", "Net Amount", "Value", "Transaction Amount", "Total", "amount"],
    config.COL_DESCRIPTION: ["Description", "Narration", "Notes", "Memo", "Details", "description"],
}


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename common header names to the names used by the project."""
    normalized = df.copy()
    rename_map = {}

    for canonical, aliases in COLUMN_ALIASES.items():
        for candidate in [canonical, *aliases]:
            if candidate in normalized.columns:
                rename_map[candidate] = canonical
                break

    if rename_map:
        normalized = normalized.rename(columns=rename_map)

    for column in config.REQUIRED_COLUMNS:
        if column not in normalized.columns:
            normalized[column] = pd.NaT if column == config.COL_DATE else (pd.NA if column == config.COL_AMOUNT else "")

    if "Region" not in normalized.columns:
        normalized["Region"] = "Unknown"
    if "Department" not in normalized.columns:
        normalized["Department"] = "Unknown"

    return normalized


def load_data(path: str = config.DEFAULT_DATA_FILE) -> pd.DataFrame:
    """Read a CSV file from disk."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find a data file at '{path}'.")
    return pd.read_csv(path, low_memory=False)


def validate_columns(df: pd.DataFrame) -> list:
    """Return any required columns that are still missing."""
    normalized = normalize_columns(df)
    return [col for col in config.REQUIRED_COLUMNS if col not in normalized.columns]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the data so it is ready for analysis."""
    df = normalize_columns(df).copy()

    df = df.dropna(how="all")
    df[config.COL_DATE] = pd.to_datetime(df[config.COL_DATE], errors="coerce")

    df[config.COL_AMOUNT] = (
        df[config.COL_AMOUNT].astype(str).str.replace(",", "", regex=False).str.strip()
    )
    df[config.COL_AMOUNT] = pd.to_numeric(df[config.COL_AMOUNT], errors="coerce")

    df[config.COL_TYPE] = df[config.COL_TYPE].astype(str).str.strip().str.title()
    df[config.COL_CATEGORY] = df[config.COL_CATEGORY].astype(str).str.strip()
    df[config.COL_DESCRIPTION] = df[config.COL_DESCRIPTION].astype(str).str.strip()

    before = len(df)
    df = df.dropna(subset=[config.COL_DATE, config.COL_AMOUNT])
    dropped_invalid = before - len(df)

    before = len(df)
    df = df.drop_duplicates()
    dropped_duplicates = before - len(df)

    df = df[df[config.COL_TYPE].isin([config.INCOME_LABEL, config.EXPENSE_LABEL])]

    df["Year"] = df[config.COL_DATE].dt.year
    df["Month"] = df[config.COL_DATE].dt.strftime("%b-%Y")
    df["MonthSortKey"] = df[config.COL_DATE].dt.strftime("%Y-%m")

    df["Region"] = df[config.COL_DESCRIPTION].str.extract(r"\b(North|South|East|West)\b", expand=False)
    df["Region"] = df["Region"].fillna("Unknown")

    df["Department"] = df[config.COL_DESCRIPTION].str.extract(r"\((Finance|Marketing|Sales|IT|Operations|HR|Admin|Support|Engineering)\s*dept\)", flags=re.I, expand=False)
    df["Department"] = df["Department"].fillna("Unknown")
    df["Department"] = df["Department"].str.title()

    df = df.sort_values(config.COL_DATE).reset_index(drop=True)
    df.attrs["rows_dropped_invalid"] = dropped_invalid
    df.attrs["rows_dropped_duplicate"] = dropped_duplicates
    return df


def load_and_clean(path: str = config.DEFAULT_DATA_FILE) -> pd.DataFrame:
    """Load a CSV and clean it in one step."""
    raw_df = load_data(path)
    normalized_df = normalize_columns(raw_df)
    missing = validate_columns(normalized_df)
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(missing)}")
    return clean_data(normalized_df)
