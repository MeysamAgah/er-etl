# TGJU Market ETL Pipeline using Apache Airflow
## Overview

This project demonstrates a complete ETL pipeline using **Apache Airflow** for orchestration and **Apache Hamilton** for data transformation mapping.

The pipeline extracts historical exchange-rate data from the TGJU API, performs modular data transformation using Hamilton micro-functions, and loads the cleaned data into a SQLite database.

The repository is intentionally organized so that Airflow is responsible only for task scheduling while the business logic and DataFrame operations are contained cleanly within Hamilton DAGs in the `src` package.

## Architecture
```
TGJU API
    │
    ▼
Extract Task (Airflow)
    │
    ▼
Transform Task (Airflow + Hamilton Driver)
    │
    ▼
Load Task (Airflow)
    │
    ▼
SQLite Database
```

## Project Structure
```
configs/
    etl.py

dags/
    etl_dag.py

src/
    scrape.py
    clean.py
    load.py

data/
```

## Technologies
* Python
* Apache Airflow
* Apache Hamilton
* Pandas
* Requests
* SQLite
* JDatetime

## ETL Steps

### Extract
* Sends HTTP request to TGJU API
* Parses API response
* Pushes parsed data to Airflow

### Transform
* Utilizes **Apache Hamilton** to define transformations as a directed acyclic graph (DAG) of Python functions.
* Converts parsed data to Pandas DataFrame
* Removes commas and handles percent symbols
* Casts numeric columns independently
* Casts Gregorian and Jalali dates

### Load
* Loads cleaned DataFrame into SQLite
* Creates the table automatically if necessary

## Running the DAG
The DAG file is located inside
```
dags/etl_dag.py
```
Copy or symlink it into your Airflow DAG directory.
Example:
```
AIRFLOW_HOME/
    dags/
        etl_dag.py
```
Make sure your project directory is available in `PYTHONPATH` so Airflow can import the `src` and `configs` packages. <br>
Then start Airflow:
```bash
airflow scheduler
```
In another terminal:
```bash
airflow webserver
```
Open
```
http://localhost:8080
```
Enable **tgju_etl** and trigger the DAG.
## Example DAG

```
extract
     │
     ▼
transform
     │
     ▼
load
```

## Output
The pipeline creates
```
data/tgju.db
```
containing
```
market_data
```

## Future Improvements
* PostgreSQL instead of SQLite
* Docker Compose deployment
* Airflow Variables & Connections
* Retry policies
* Incremental loading
* Logging
* Unit tests
* Data quality validation
* Object storage staging (Parquet)