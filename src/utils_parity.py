from web3 import Web3, HTTPProvider
from web3.exceptions import BadFunctionCallOutput, SolidityError
import json


def get_contract_decimals(token_address, parity_url):
    """ Get decimals from Parity node for ERC20 token
    :param token_address: address of ERC20 token contract
    :param parity_url: Parity node URL
    """
    with open("src/erc20_abi.json") as f:
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
