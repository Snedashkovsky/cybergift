from google.cloud import bigquery, bigquery_storage
from google.oauth2 import service_account


PROJECT_ID = 'cosmic-keep-223223'
DATASET_NAME = 'gas_analysis'
INITIAL_TS = '2015-07-30 00:00:00'
SNAPSHOT_TS = '2021-03-02 00:00:00'


# Construct a BigQuery client object.
KEY_PATH = "bigquery_project.json"

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

bqstorage_client = bigquery_storage.BigQueryReadClient(credentials=credentials)
