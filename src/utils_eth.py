import json
from web3 import Web3, HTTPProvider
from web3.exceptions import BadFunctionCallOutput, SolidityError
from cachetools.func import ttl_cache

from config import ETH_URL, SNAPSHOT_BLOCKNUMBER


@ttl_cache(maxsize=128, ttl=100)
def get_w3_and_contract_object(
        token_address: str,
        eth_url: str,
        erc20_abi_url: str):
    """
    Get w3 and contract object
    :param token_address: address of ERC20 token contract
    :param eth_url: Ethereum node URL
    :param erc20_abi_url: URL of ERC20 ABI
    :return:
    """
    with open(erc20_abi_url) as _f:
        _contract_abi = json.load(_f)
    w3 = Web3(HTTPProvider(eth_url))
    return w3, w3.eth.contract(w3.toChecksumAddress(token_address), abi=_contract_abi)


def get_contract_decimals(
        token_address: str,
        eth_url: str = ETH_URL,
        erc20_abi_url: str = "src/erc20_abi.json",
        print_messages: bool = True) -> int:
    """ Get decimals from Ethereum node for ERC20 token
    :param token_address: address of ERC20 token contract
    :param eth_url: Ethereum node URL
    :param erc20_abi_url: URL of ERC20 ABI
    :param print_messages: Print error messages or not
    """

    _w3, _contract = get_w3_and_contract_object(
        token_address=token_address,
        eth_url=eth_url,
        erc20_abi_url=erc20_abi_url)
    try:
        decimals = _w3.toInt(_contract.functions.decimals().call())
    except BadFunctionCallOutput as e:
        decimals = -1
        if print_messages:
            print(f'BadFunctionCallOutput {e}')
    except SolidityError as e:
        decimals = -1
        if print_messages:
            print(f'SolidityError {e}')
    except ValueError as e:
        decimals = -1
        if print_messages:
            print(f'ValueError {e}')
    return decimals


def get_balance(
        owner_address: str,
        token_address: str,
        block_number: int = SNAPSHOT_BLOCKNUMBER,
        eth_url: str = ETH_URL,
        erc20_abi_url: str = "src/erc20_abi.json",
        print_messages: bool = True) -> int:
    """
    Get ERC20 balance from Ethereum node for given owner address, block number and ERC20 token
    :param owner_address: owner address of ERC20 token
    :param token_address: address of ERC20 token contract
    :param block_number: block number for getting data (!ARCHIVAL NODE NEEDED! or set -1)
    :param eth_url: Ethereum node URL
    :param erc20_abi_url: URL of ERC20 ABI
    :param print_messages: Print error messages or not
    :return:
    """
    _w3, _contract = get_w3_and_contract_object(
        token_address=token_address,
        eth_url=eth_url,
        erc20_abi_url=erc20_abi_url)
    try:
        balance = _w3.toInt(_contract.functions.balanceOf(_w3.toChecksumAddress(owner_address)).call(
            block_identifier=block_number))
    except BadFunctionCallOutput as e:
        balance = 0
        if print_messages:
            print(f'BadFunctionCallOutput {e}')
    except SolidityError as e:
        balance = -1
        if print_messages:
            print(f'SolidityError {e}')
    except ValueError as e:
        balance = -1
        if print_messages:
            print(f'ValueError {e}')
    if print_messages:
        print(f'balance {balance}')
    return balance
