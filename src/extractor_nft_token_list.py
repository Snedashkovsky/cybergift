import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm_notebook

from config import BEAUTIFULSOUP_HEADERS, ETHERSCAN_NFT_URL, ETHERSCAN_NFT_LAST_PAGE_NUMBER, ETHERSCAN_NFT_CSV_NAME


def extract_nft_tokens(headers=BEAUTIFULSOUP_HEADERS,
                       url=ETHERSCAN_NFT_URL,
                       last_page_number=ETHERSCAN_NFT_LAST_PAGE_NUMBER,
                       csv_name=ETHERSCAN_NFT_CSV_NAME):
    """
    Extract names, addresses and descriptions for NFT tokens from Etherscan
    :param headers: headers for page request
    :param url: page url for Etherscan NFT Tokens
    :param last_page_number: number of the last page for Etherscan NFT Tokens
    :param csv_name: csv name for saving NFT tokens data
    :return: True if successful or False otherwise.
    """
    page_queries = [''] + [f'?p={item}' for item in range(2, last_page_number + 1)]

    nft_tokens_data = []

    for page_query in tqdm_notebook(page_queries):
        page = requests.get(url + page_query,
                            headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        for row in soup.find(id='tblResult').find_all('tr')[1:]:
            # Extract token address from link
            try:
                token_address = row.find('a', class_="text-primary")['title']
            except (AttributeError, KeyError):
                token_address = ''
            # Extract token name from link
            try:
                token_name = row.find('a', class_="text-primary").text
            except (AttributeError, KeyError):
                token_name = ''
            # Extract token description
            try:
                token_description = row.find('p', class_="d-none d-md-block font-size-1 mb-0").text
            except (AttributeError, KeyError):
                token_description = ''
            # Write results
            if token_address != '':
                nft_tokens_data.append([token_name, token_address[:42], token_description])
            elif token_name != '':
                nft_tokens_data.append(['', token_name[:42], token_description])
            else:
                print(f'The row was scripted. Error token address in the: \n{row}')

    print(f'Extracted {len(nft_tokens_data)} tokens')

    if len(nft_tokens_data) > 0:
        nft_tokens_df = pd.DataFrame(nft_tokens_data,
                                     columns=['token_name', 'token_address', 'description'])
        nft_tokens_df.to_csv(csv_name)
        return True
    return False
