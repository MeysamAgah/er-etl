from datetime import datetime

import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator

from configs.etl import (
    DATABASE_PATH,
    TABLE_NAME,
    COLUMNS,
    ER_TYPE,
    API_LENGTH,
)

from src.scrape import fetch_market_data
from src.clean import dict_to_dataframe, clean_dataframe
from src.load import load_dataframe


def extract(ti):

    parsed = fetch_market_data(
        er_type=ER_TYPE,
        columns=COLUMNS,
        length=API_LENGTH,
    )

    ti.xcom_push(
        key="parsed",
        value=parsed,
    )


def transform(ti):

    parsed = ti.xcom_pull(
        task_ids="extract",
        key="parsed",
    )

    df = dict_to_dataframe(parsed)

    df = clean_dataframe(df)

    output_path = "/opt/airflow/data/processed/clean_data.parquet"

    df.to_parquet(
        output_path,
        index=False,
    )

    ti.xcom_push(
        key="clean_path",
        value=output_path,
    )


def load(ti):

    path = ti.xcom_pull(
        task_ids="transform",
        key="clean_path",
    )

    df = pd.read_parquet(path)

    load_dataframe(
        df=df,
        database_path=DATABASE_PATH,
        table_name=TABLE_NAME,
    )


with DAG(
    dag_id="tgju_etl",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["etl", "sqlite"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
    )

    extract_task >> transform_task >> load_task