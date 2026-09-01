import os
from datetime import datetime
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import Hamilton driver
from hamilton import driver
from hamilton_sdk import adapters as hamilton_adapters

from configs.etl import (
    DATABASE_PATH,
    TABLE_NAME,
    COLUMNS,
    ER_TYPE,
    API_LENGTH,
)

from src.scrape import fetch_market_data
from src.load import load_dataframe
import src.clean as clean_module


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

    # 1. Convert Dictionary directly to a DataFrame
    raw_df = pd.DataFrame(parsed["rows"])

    # 2. Add prefix to inputs to match the expected parameter names in Hamilton 
    # (e.g. column 'open' becomes 'raw_open' so it doesn't conflict with target column 'open')
    raw_df = raw_df.add_prefix("raw_")

    tracker = hamilton_adapters.HamiltonTracker(
        project_id=1,
        username="meysam.agah",       # same email you signed in with
        dag_name="my_version_of_the_dag",
        tags={"environment": "dev"},
        hamilton_api_url=os.environ.get("HAMILTON_API_URL", "http://localhost:8241"),
    )

    # 3. Setup Hamilton Driver
    dr = (
        driver.Builder()
        .with_modules(clean_module)
        .with_adapters(tracker)
        .build()
    )

    # 4. Define expected outputs & Execute Hamilton Graph
    output_columns = [
        "open", "high", "low", "close", "change",
        "change_percent", "gregorian_date", "jalali_date"
    ]
    inputs = raw_df.to_dict(orient="series")
    df = dr.execute(output_columns, inputs=inputs)

    # 5. Output Data
    output_path = "/opt/airflow/data/processed/clean_data.parquet"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
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
    tags=["etl", "sqlite", "hamilton"],
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