from google.cloud import bigquery, bigquery_storage
from google.oauth2 import service_account


INITIAL_TS = '2015-07-30 00:00:00'
SNAPSHOT_TS = '2021-03-02 00:00:00'

PROJECT_ID = 'cosmic-keep-223223'

ETH_ANALYSIS_TYPE = 'Average Citizens. ETH Analysis'
ETH_ANALYSIS_DATASET_NAME = 'eth_analysis'
ETH_ANALYSIS_DISTRIBUTION_TABLE_NAME = 'eth_analysis_distribution'

ERC20_ANALYSIS_TYPE = 'Passionate Investors. ERC20 Analysis'
ERC20_ANALYSIS_DATASET_NAME = 'erc20_analysis'
ERC20_BALANCES_TABLE_NAME = 'erc20_balances'
ERC20_ANALYSIS_DISTRIBUTION_TABLE_NAME = 'erc20_analysis_distribution'
ERC20_TOKEN_METADATA_TABLE_NAME = 'erc20_token_metadata'

GAS_ANALYSIS_TYPE = 'Extraordinary Hackers. Gas Analysis'
GAS_ANALYSIS_DATASET_NAME = 'gas_analysis'
GAS_SPEND_BY_CONTRACT_TABLE_NAME = 'gas_spend_by_contract'
GAS_ANALYSIS_DISTRIBUTION_TABLE_NAME = 'gas_analysis_distribution'

FINAL_DATASET_NAME = 'final'
FINAL_DISTRIBUTION_VIEW_NAME = 'final_distribution'


# Construct a BigQuery client object.
KEY_PATH = "bigquery_project.json"

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

bqstorage_client = bigquery_storage.BigQueryReadClient(credentials=credentials)
