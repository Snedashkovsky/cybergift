import json
from web3 import Web3, HTTPProvider
from web3.exceptions import BadFunctionCallOutput, SolidityError

from config import ETH_URL


def get_contract_decimals(
        token_address: str,
        eth_url: str = ETH_URL,
        erc20_abi_url: str = "src/erc20_abi.json",
        print_messages: bool = True):
    """ Get decimals from Parity node for ERC20 token
    :param token_address: address of ERC20 token contract
    :param eth_url: Ethereum node URL
    :param erc20_abi_url: URL of ERC20 ABI
    :param print_messages: Print error messages or not
    """
    with open(erc20_abi_url) as f:
        contract_abi = json.load(f)
    w3 = Web3(HTTPProvider(eth_url))
    token_info = w3.eth.contract(w3.toChecksumAddress(token_address), abi=contract_abi)
    try:
        decimals = w3.toInt(token_info.functions.decimals().call())
    except BadFunctionCallOutput as e:
        decimals = -1
        if print_messages:
            print(f'BadFunctionCallOutput {e}')
    except SolidityError as e:
        decimals = -1
        if print_messages:
            print(f'SolidityError {e}')
    return decimals
