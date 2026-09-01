import pandas as pd

def _clean_numeric_column(series: pd.Series, dtype: str = "int32") -> pd.Series:
    """
    Helper function to clean numeric strings.
    Prefixed with an underscore so Hamilton ignores it as a DAG node.
    """
    series = (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .replace("-", None)
    )

    return (
        pd.to_numeric(series, errors="coerce")
        .fillna(0)
        .astype(dtype)
    )


def open(raw_open: pd.Series) -> pd.Series:
    return _clean_numeric_column(raw_open, "int32")


def high(raw_high: pd.Series) -> pd.Series:
    return _clean_numeric_column(raw_high, "int32")


def low(raw_low: pd.Series) -> pd.Series:
    return _clean_numeric_column(raw_low, "int32")


def close(raw_close: pd.Series) -> pd.Series:
    return _clean_numeric_column(raw_close, "int32")


def change(raw_change: pd.Series) -> pd.Series:
    return _clean_numeric_column(raw_change, "int32")


def change_percent(raw_change_percent: pd.Series) -> pd.Series:
    series = raw_change_percent.astype(str).str.replace("%", "", regex=False)
    return _clean_numeric_column(series, "float64")


def gregorian_date(raw_gregorian_date: pd.Series) -> pd.Series:
    return pd.to_datetime(raw_gregorian_date, format="%Y/%m/%d")


def jalali_date(raw_jalali_date: pd.Series) -> pd.Series:
    return raw_jalali_date.astype(str)