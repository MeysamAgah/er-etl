# TGJU Market ETL Pipeline using Apache Airflow
## Overview

This project demonstrates a complete ETL pipeline using **Apache Airflow**.

The pipeline extracts historical exchange-rate data from the TGJU API, performs data cleaning using Pandas, and loads the cleaned data into a SQLite database.

The repository is intentionally organized so that Airflow is responsible only for orchestration while the business logic remains reusable inside the src package.

## Architecture
```
TGJU API
    │
    ▼
Extract Task
    │
    ▼
Transform Task
    │
    ▼
Load Task
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
* Converts parsed data to Pandas DataFrame
* Removes commas
* Converts numeric columns
* Converts Gregorian dates
* Converts Jalali dates

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