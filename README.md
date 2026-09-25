<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0a0f,50:1a1a2e,100:6366f1&height=200&section=header&text=GCP%20DBT%20Project&fontSize=40&fontColor=e2e8f0&fontAlignY=35&desc=End-to-End%20ELT%20Pipeline%20%7C%20dbt%20%2B%20BigQuery%20%7C%20GCP&descAlignY=55&descSize=18&descColor=94a3b8"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=6366F1&center=true&vCenter=true&width=600&lines=Finance+Transactions+ELT+Pipeline;Raw+Data+%E2%86%92+GCS+%E2%86%92+BigQuery;dbt+Staging+%7C+Intermediate+%7C+Marts;Data+Quality+Tests+with+dbt" alt="Typing SVG" />

</div>

---

A production-style ELT pipeline built on **Google Cloud Platform** using **dbt + BigQuery**.
Raw finance transaction data flows from a CSV file into Google Cloud Storage, gets loaded into
BigQuery, and is transformed through three dbt layers into a clean reporting table ready for
Looker Studio dashboards.

---

### Architecture

```
raw_transactions.csv
        ↓
Google Cloud Storage (GCS)
        ↓
load_to_bigquery.py
        ↓
BigQuery Raw Table  →  raw.transactions
        ↓
dbt stg_transactions   →  clean & cast columns
        ↓
dbt int_transactions   →  business logic, amount category
        ↓
dbt fct_transactions   →  net balance per customer per month
        ↓
Looker Studio Dashboard
```

---

### Project Structure

```
├── raw_transactions.csv                  # sample raw finance data
├── load_to_bigquery.py                   # loads GCS → BigQuery raw table
├── requirements.txt                      # python dependencies
├── dbt_project.yml                       # dbt project config
└── models/
    ├── schema.yml                        # data quality tests + docs
    ├── staging/
    │   └── stg_transactions.sql          # clean & rename raw columns
    ├── intermediate/
    │   └── int_transactions.sql          # business logic & enrichment
    └── marts/
        └── fct_transactions.sql          # final aggregated reporting table
```

---

### dbt Layers

| Layer | Model | What it does |
|-------|-------|-------------|
| Staging | `stg_transactions` | Cleans and casts raw columns, filters nulls |
| Intermediate | `int_transactions` | Filters completed txns, splits credit/debit, adds amount category |
| Marts | `fct_transactions` | Aggregates net balance, total credits/debits per customer per month |

---

### Data Quality Tests

- `txn_id` — unique + not null
- `txn_type` — accepted values: `credit`, `debit`
- `status` — accepted values: `completed`, `pending`, `failed`
- `amount_category` — accepted values: `high`, `medium`, `low`

---

### Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Looker Studio](https://img.shields.io/badge/Looker_Studio-4285F4?style=for-the-badge&logo=looker&logoColor=white)

</div>

---

### Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Configure GCP credentials**

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

**3. Load raw data to BigQuery**
```bash
python load_to_bigquery.py
```

**4. Run dbt**
```bash
dbt debug    # test BigQuery connection
dbt run      # run all models
dbt test     # run data quality tests
```

---

### Author

<div align="center">

[![Portfolio](https://img.shields.io/badge/Portfolio-6366f1?style=for-the-badge&logo=vercel&logoColor=white)](https://mohammed-junaid-khan.vercel.app)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mohammed-junaid-khan/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mohammedjunaidkhan990-del)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:Junaidkhan91020@gmail.com)

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6366f1,50:1a1a2e,100:0a0a0f&height=100&section=footer"/>

*"Data is only useful when it's clean, tested, and trusted."*

</div>
