import json
from web3 import Web3, HTTPProvider
from web3.exceptions import BadFunctionCallOutput, SolidityError

from config import PARITY_URL


def get_contract_decimals(token_address, parity_url=PARITY_URL, erc20_abi_url="src/erc20_abi.json"):
    """ Get decimals from Parity node for ERC20 token
    :param token_address: address of ERC20 token contract
    :param parity_url: Parity node URL
    :param erc20_abi_url: URL of ERC20 ABI
    """
    with open(erc20_abi_url) as f:
        contract_abi = json.load(f)
    w3 = Web3(HTTPProvider(parity_url))
    token_info = w3.eth.contract(w3.toChecksumAddress(token_address), abi=contract_abi)
    try:
        decimals = w3.toInt(token_info.functions.decimals().call())
    except BadFunctionCallOutput as e:
        decimals = -1
        print(e)
    except SolidityError as e:
        decimals = -1
        print(e)
    return decimals
