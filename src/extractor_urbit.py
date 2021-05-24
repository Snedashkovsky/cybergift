import json
import logging
import multiprocessing as mp
from itertools import chain
import pandas as pd
from web3 import Web3, HTTPProvider

from config import ETH_URL, SNAPSHOT_BLOCKNUMBER

logging.basicConfig(filename='error_blocks.log', level=logging.ERROR)

AZIMUTH_TOKEN_CONTRACT_ADDRESS = '0x6ac07b7c4601b5ce11de8dfe6335b871c7c4dd4d'.lower()
AZIMUTH_CONTRACT_ADDRESS = '0x223c067F8CF28ae173EE5CafEa60cA44C335fecB'.lower()
AZIMUTH_CONTRACT_ABI_URL = 'src/azimuth_abi.json'
LINEAR_STAR_RELEASE_CONTRACT_ADDRESS = '0x86cd9cd0992F04231751E3761De45cEceA5d1801'.lower()
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

POINT_DICT = {
    0: ['galaxy', 0],
    1: ['star', 8],
    2: ['planet', 16]
}

with open(AZIMUTH_CONTRACT_ABI_URL) as f:
    AZIMUTH_CONTRACT_ABI = json.load(f)

w3 = Web3(HTTPProvider(ETH_URL))
contract = w3.eth.contract(
    address=w3.toChecksumAddress(AZIMUTH_CONTRACT_ADDRESS),
    abi=AZIMUTH_CONTRACT_ABI)


def _get_point_data(point: int,
                    block_number: int = SNAPSHOT_BLOCKNUMBER):
    """
    Get and calculate data for given point id
    :param point: point id
    :param block_number: snapshot block number
    :return: list of point data
    """
    owner = str(contract.functions.getOwner(int(point)).call({'defaultBlock': block_number})).lower()
    point_size = contract.functions.getPointSize(int(point)).call()
    point_type = POINT_DICT[point_size][0]
    parent_point = int(point) % 2**POINT_DICT[point_size][1]
    return [point, point_size, point_type, owner, parent_point]


def _get_point_data_from_chunk(point_chunk: list):
    """
    Get and calculate data for point chunk
    :param point_chunk: chunk with list of points
    :return: list of chunk point data
    """
    point_data = list()
    for point in point_chunk:
        point_data.append(_get_point_data(point))
    print(f'Points {point_chunk[0]}:{point_chunk[-1]} extracted')
    return point_data


def _chunks(lst: list,
            chunk_size: int):
    """
    Split list by chunks
    :param lst: flat list for splitting by chunks
    :param chunk_size: Number of items in a chunk
    :return: list of chunk lists
    """
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def extract_point_data(point_list: list,
                       pool_size: int = 4,
                       chunk_size: int = 128):
    """
    Extract point data from a ethereum node
    :param point_list: Point list for extracting data
    :param pool_size: Number of parallel workers
    :param chunk_size: Number of items in a chunk
    :return: DataFrame with point data
    """
    chunks_list = list(_chunks(point_list, chunk_size=chunk_size))
    print(f'Processing {len(point_list)} points split into {len(chunks_list)} chunks on {pool_size} processes:')

    p = mp.Pool(pool_size)
    point_data_list = p.map(_get_point_data_from_chunk, chunks_list)

    point_data_df = pd.DataFrame(chain(*point_data_list),
                                 columns=['point', 'point_size', 'point_type', 'owner', 'parent_point'])
    point_data_df.to_csv('data/point_data.csv')
    return point_data_df
