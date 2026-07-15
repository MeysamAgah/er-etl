import sqlite3


def load_dataframe(df, database_path, table_name):
    """
    Load dataframe into sqlite.
    """

    conn = sqlite3.connect(database_path)

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False,
    )

    conn.close()