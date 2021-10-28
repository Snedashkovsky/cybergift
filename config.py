from google.cloud import bigquery, bigquery_storage
from google.oauth2 import service_account
from dotenv import dotenv_values

INITIAL_TS = '2015-07-30 00:00:00'
SNAPSHOT_TS = '2021-05-01 00:00:00'
SNAPSHOT_BLOCKNUMBER = 12_344_945
TARGET_GRADE_SHARES = (0.89, 0.99)

PROJECT_ID = 'cosmic-keep-223223'

CITIZENS_AUDIENCE = 'Average Citizens. ETH Analysis'
ETH_ANALYSIS_DATASET_NAME = 'eth_analysis'
ETH_ANALYSIS_DISTRIBUTION_TABLE_NAME = 'eth_analysis_distribution'

CYBERPUNKS_AUDIENCE = 'Cyberpunks. ERC20 and ERC721 Analysis'

HACKERS_AUDIENCE = 'Extraordinary Hackers. Gas Analysis'
GAS_ANALYSIS_DATASET_NAME = 'gas_analysis'
GAS_SPEND_BY_CONTRACT_TABLE_NAME = 'gas_spend_by_contract'
GAS_ANALYSIS_DISTRIBUTION_TABLE_NAME = 'gas_analysis_distribution'

LEADERS_AUDIENCE = 'Key Opinion Leaders. ERC20 Analysis'
LEADERS_SEGMENT = 'Top Token Holders'
ERC20_TOP_DISTRIBUTION_TABLE_NAME = 'erc20_top_distribution'

MASTERS_AUDIENCE = 'Masters of the Great Web. Gas and ERC721 Analysis'
ERC721_ANALYSIS_DATASET_NAME = 'erc721_analysis'
ERC721_ROW_AMOUNT_TABLE_NAME = 'erc721_row_amounts'
ERC721_NFT_TOKEN_TABLE_NAME = 'nft_tokens'
ERC721_TOKEN_TABLE_NAME = 'erc721_tokens'
ERC721_AMOUNT_TABLE_NAME = 'erc721_amounts'
ERC721_ANALYSIS_DISTRIBUTION_TABLE_NAME = 'erc721_analysis_distribution'
AZIMUTH_POINTS_TABLE_NAME = 'azimuth_points'

INVESTORS_AUDIENCE = 'Passionate Investors. ERC20 Analysis'
ERC20_ANALYSIS_DATASET_NAME = 'erc20_analysis'
ERC20_ROW_BALANCES_TABLE_NAME = 'erc20_row_balances'
ERC20_REVISED_BALANCES_TABLE_NAME = 'erc20_revised_balances'
ERC20_BALANCES_TABLE_NAME = 'erc20_balances'
STABLECOINS_LOVERS_TABLE_NAME = 'stablecoins_lovers'
ERC20_ANALYSIS_DISTRIBUTION_TABLE_NAME = 'erc20_analysis_distribution'
ERC20_TOKEN_METADATA_TABLE_NAME = 'erc20_token_metadata'

HEROES_AUDIENCE = 'Heroes of the Great Web. Genesis and ETH2 Stakers'
GENESIS_AND_ETH2_DATASET_NAME = 'genesis_and_eth2_stakers'
GENESIS_AND_ETH2_DISTRIBUTION_TABLE_NAME = 'genesis_and_eth2_stakers_distribution'

MANUAL_ADDRESSES_AUDIENCE = 'CEXes'
MANUAL_ADDRESSES_SEGMENT = 'Manual Set Addresses'
MANUAL_ADDRESSES_DATASET_NAME = 'manual_addresses'
MANUAL_ADDRESSES_DISTRIBUTION_TABLE_NAME = 'manual_addresses_distribution'

COSMOS_AUDIENCE = 'Astronauts. ATOM Analysis'
COSMOS_SEGMENT = 'ATOM Balances'
COSMOS_DATASET_NAME = 'cosmos'
COSMOS_DISTRIBUTION_TABLE_NAME = 'cosmos_distribution'

FINAL_DATASET_NAME = 'final'
CONTRACT_ADDRESSES_TABLE = 'contract_addresses'
DISTRIBUTION_TABLE_NAME = 'distribution_without_gift_size'
FINAL_DISTRIBUTION_TABLE_NAME = 'final_distribution'
GIFT_PER_ADDRESS_PIVOT_TABLE_NAME = 'gift_per_address_pivot'

# Etherscan extractor
BEAUTIFULSOUP_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
  }
ETHERSCAN_NFT_URL = 'https://etherscan.io/tokens-nft'
ETHERSCAN_NFT_LAST_PAGE_NUMBER = 206
ETHERSCAN_NFT_CSV_NAME = 'data/etherscan_erc721.csv'

# Construct a BigQuery client object.
KEY_PATH = "bigquery_project.json"

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

ETH_URL = dotenv_values(".env")['ETH_URL']

bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

bqstorage_client = bigquery_storage.BigQueryReadClient(credentials=credentials)
