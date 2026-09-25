# GCP DBT Project — Finance Transactions ELT Pipeline

An end-to-end ELT pipeline built with **dbt + BigQuery** on Google Cloud Platform.

## Architecture

```
raw_transactions.csv
        ↓
Google Cloud Storage (GCS)
        ↓
load_to_bigquery.py
        ↓
BigQuery Raw Table (raw.transactions)
        ↓
dbt stg_transactions   → clean & cast columns
        ↓
dbt int_transactions   → business logic, amount category
        ↓
dbt fct_transactions   → aggregated net balance per customer
        ↓
Looker Studio Dashboard
```

## Tech Stack

- **Google Cloud Storage** — raw file storage
- **BigQuery** — data warehouse
- **dbt** — data transformation
- **Looker Studio** — visualization
- **Python** — GCS to BigQuery loader

## Project Structure

```
├── raw_transactions.csv          # sample raw data
├── load_to_bigquery.py           # loads GCS → BigQuery
├── requirements.txt              # python dependencies
├── dbt_project.yml               # dbt project config
└── models/
    ├── schema.yml                # tests + documentation
    ├── staging/
    │   └── stg_transactions.sql  # clean raw data
    ├── intermediate/
    │   └── int_transactions.sql  # business logic
    └── marts/
        └── fct_transactions.sql  # final reporting table
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure GCP credentials
Create a `profiles.yml` in the project root (not committed for security):
```yaml
dbt_bigquery_project:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: <your-gcp-project-id>
      dataset: dbt_dev
      keyfile: <path-to-service-account.json>
      threads: 4
      location: US
```

### 3. Load raw data to BigQuery
```bash
python load_to_bigquery.py
```

### 4. Run dbt
```bash
dbt debug    # test BigQuery connection
dbt run      # run all models
dbt test     # run data quality tests
```

## dbt Models

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_transactions` | Staging | Cleans and casts raw columns |
| `int_transactions` | Intermediate | Filters completed txns, adds credit/debit split and amount category |
| `fct_transactions` | Marts | Aggregates net balance, total credits/debits per customer per month |

## Data Quality Tests

- `txn_id` — unique + not null
- `txn_type` — accepted values: credit, debit
- `status` — accepted values: completed, pending, failed
- `amount_category` — accepted values: high, medium, low
