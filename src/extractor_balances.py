from threading import Thread
from queue import Queue
import logging
import pandas as pd

from src.utils_eth import get_balance
from src.utils_bigquery import get_df
from config import PROJECT_ID, ERC20_ROW_BALANCES_TABLE_NAME, ERC20_ANALYSIS_DATASET_NAME


def _get_address_and_token(token_address: str, limit: int) -> pd.DataFrame:
    """
    Get dataframe with non-zero balance addresses from ERC20 Raw table for given token address
    :param token_address: token address
    :param limit: maximum number of addresses
    :return: Pandas dataframe with addresses and token addresses
    """
    _query = f'''
        SELECT
             address,
             token_address
        FROM `{PROJECT_ID}.{ERC20_ANALYSIS_DATASET_NAME}.{ERC20_ROW_BALANCES_TABLE_NAME}`
        WHERE token_address='{token_address}'
          AND balance != 0
        LIMIT {limit}
    '''
    return get_df(_query)


def _get_balance_for_queue(source_q: Queue, result_q: Queue) -> None:
    """
    Get address balances from ETH node
    :param source_q: source queue with addresses and token addresses data
    :param result_q: result query for putting addresses, token addresses and balances
    :return: None
    """
    while not source_q.empty():
        _item = source_q.get()
        _balance = get_balance(_item[0], _item[1], print_messages=False)
        if _balance >= 0:
            result_q.put([_item[0], _item[1], _balance])
            logging.info(f'address {_item[0]} token {_item[1]} balance {_balance:>,}')
        else:
            logging.error(f'Error in address {_item[0]} token {_item[1]} balance {_balance:>,}')
        source_q.task_done()


def get_balances(
        token_address: str = '0x0000000000b3f879cb30fe243b4dfee438691c04',
        limit: int = 1000000,
        threads_number: int = 10) -> pd.DataFrame:
    """
    Extract balances from ETH node for given token address
    :param token_address: token address
    :param limit: maximum number of addresses
    :param threads_number: number of threads for extractor from ETH node
    :return: Pandas dataframe with addresses, token addresses and balances
    """
    logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s',
                        level=logging.ERROR)

    _address_and_token_queue = Queue()
    _result_queue = Queue()

    _address_and_token_df = _get_address_and_token(token_address=token_address, limit=limit)
    _address_and_token_list = _address_and_token_df[['address', 'token_address']].values.tolist()
    print(f'Uploaded {len(_address_and_token_df):>,} addresses. Start getting balances...')

    for _address_and_token in _address_and_token_list:
        _address_and_token_queue.put(_address_and_token)

    # create and run threads
    _threads = [
      Thread(target=_get_balance_for_queue, args=(_address_and_token_queue, _result_queue, ))
      for _ in range(threads_number)
    ]
    for _thread in _threads:
        _thread.start()
    for _thread in _threads:
        _thread.join()

    _result = []
    while not _result_queue.empty():
        _result.append(_result_queue.get())
    print(f'Extracted balances for {len(_address_and_token_df):>,} addresses')
    return pd.DataFrame(data=_result, columns=('address', 'token_address', 'balance'))


if __name__ == '__main__':
    print(get_balances(limit=10))
