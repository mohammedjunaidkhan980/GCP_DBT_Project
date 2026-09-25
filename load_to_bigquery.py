from google.cloud import storage
from google.cloud import bigquery
import os

# ─── GCP CONFIG ───────────────────────────────────────────────
GCP_PROJECT_ID      = "# here your GCP project id"         # e.g. my-gcp-project-123
GCS_BUCKET_NAME     = "# here your GCS bucket name"        # e.g. my-dbt-bucket
GCS_FILE_PATH       = "raw/raw_transactions.csv"             # path inside bucket
LOCAL_CSV_PATH      = "raw_transactions.csv"                # local file to upload
BQ_DATASET          = "raw"                                 # BigQuery dataset name
BQ_TABLE            = "transactions"                        # BigQuery table name
SERVICE_ACCOUNT_KEY = "# here your GCP service account json path"  # e.g. /path/to/key.json
# ──────────────────────────────────────────────────────────────

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_KEY


def upload_csv_to_gcs():
    client = storage.Client(project=GCP_PROJECT_ID)
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob   = bucket.blob(GCS_FILE_PATH)

    blob.upload_from_filename(LOCAL_CSV_PATH)
    print(f"Uploaded {LOCAL_CSV_PATH} to gs://{GCS_BUCKET_NAME}/{GCS_FILE_PATH}")


def load_gcs_to_bigquery():
    client     = bigquery.Client(project=GCP_PROJECT_ID)
    dataset_id = f"{GCP_PROJECT_ID}.{BQ_DATASET}"
    table_id   = f"{GCP_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

    # Create dataset if not exists
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    client.create_dataset(dataset, exists_ok=True)
    print(f"Dataset '{BQ_DATASET}' ready")

    # Define load job config
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # overwrite each run
    )

    gcs_uri  = f"gs://{GCS_BUCKET_NAME}/{GCS_FILE_PATH}"
    load_job = client.load_table_from_uri(gcs_uri, table_id, job_config=job_config)
    load_job.result()  # wait for job to complete

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows into {table_id}")


if __name__ == "__main__":
    upload_csv_to_gcs()
    load_gcs_to_bigquery()
