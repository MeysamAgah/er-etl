import pandas as pd
import jdatetime


def dict_to_dataframe(parsed_data):
    """
    Convert parsed TGJU data into a pandas DataFrame.

    Parameters
    ----------
    parsed_data : dict
        Output of parse_er_data().

    Returns
    -------
    pandas.DataFrame
    """
    return pd.DataFrame(parsed_data["rows"])


def clean_numeric_column(series, dtype="int32"):
    """
    Clean a numeric column by:
    - removing commas
    - converting '-' to missing values
    - coercing invalid values to NaN
    - filling missing values with 0
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

def clean_dataframe(df):
    """
    Clean TGJU market data.

    Operations
    ----------
    - Remove commas from price columns
    - Convert prices to int32
    - Convert change to int32
    - Convert change_percent to float
    - Convert gregorian_date to datetime64
    - Convert jalali_date to jdatetime.date
    """

    df = df.copy()

    int_columns = [
        "open",
        "high",
        "low",
        "close",
        "change",
    ]

    for col in int_columns:
        df[col] = clean_numeric_column(df[col], "int32")

    # Percent column
    df["change_percent"] = clean_numeric_column(
        df["change_percent"].str.replace("%", "", regex=False),
        "float64",
    )
    # Gregorian date
    df["gregorian_date"] = pd.to_datetime(
        df["gregorian_date"],
        format="%Y/%m/%d"
    )

    df["jalali_date"] = df["jalali_date"].astype(str)

    return df