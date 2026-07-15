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

    # Integer columns containing commas
    int_columns = ["open", "high", "low", "close"]

    for col in int_columns:
        df[col] = (
            df[col]
            .str.replace(",", "", regex=False)
            .astype("int32")
        )

    # Change column
    df["change"] = (
        df["change"]
        .replace("-", "0")
        .astype("int32")
    )

    # Percent column
    df["change_percent"] = (
        df["change_percent"]
        .replace("-", "0")
        .str.replace("%", "", regex=False)
        .astype(float)
    )

    # Gregorian date
    df["gregorian_date"] = pd.to_datetime(
        df["gregorian_date"],
        format="%Y/%m/%d"
    )

    # Jalali date
    def to_jalali(value):
        y, m, d = map(int, value.split("/"))
        return jdatetime.date(y, m, d)

    df["jalali_date"] = df["jalali_date"].apply(to_jalali)

    return df