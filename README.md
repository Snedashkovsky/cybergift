# cyberGift

Gift for Ethereum users that will maximize the initial usage of Cyber by the following audiences:

- true heroes of the Great Web
- extraordinary hackers
- average citizens
- masters of the Great Web
- passionate investors
- key opinion leaders
- inborn entrepreneurs
- cyberpunks  

The purpose of the research is to incentivize and inspire (at least 100k) the most web3 power-users to try out Cyber.

Ethereum addresses have to be labeled by the audiences and differentiated into three power grades for every audience 
in such a way to create also non-fungible tokens.

The research results have to be in the form of reproducible scripts that will be pull requested in the 
[launch-kit](https://github.com/cybercongress/launch-kit), and an article with the rationale of the gift structure.

Data source is [BigQuery crypto-ethereum dataset](https://console.cloud.google.com/bigquery?d=crypto_ethereum&p=bigquery-public-data&page=dataset&project=cosmic-keep-223223) 
by [Blockchain ETL](https://github.com/blockchain-etl).

Research is done on the [proposal](https://cyber.page/governance/20) basis.

## Basic Assumptions

### Distribution between Audiences

Distribution between **audiences**:
<table style="text-align: left">
    <thead style="text-align: center">
        <tr>
            <th>Audience</th>
            <th>Share of Total Supply</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align: left"> Astronauts </td>
            <td style="text-align: center"> 1% </td>
        </tr>
        <tr>
            <td style="text-align: left"> Average Citizens </td>
            <td style="text-align: center"> 35% </td>
        </tr>
        <tr>
            <td style="text-align: left"> Cyberpunks </td>
            <td style="text-align: center"> 2% </td>
        </tr>
        <tr>
            <td style="text-align: left"> Extraordinary Hackers </td>
            <td style="text-align: center"> 7% </td>
        </tr>
        <tr>
            <td style="text-align: left"> Key Opinion Leaders </td>
            <td style="text-align: center"> 2% </td>
        </tr>
        <tr>
            <td style="text-align: left"> Masters of the Great Web </td>
            <td style="text-align: center"> 13% </td>
        </tr>
        <tr>
            <td style="text-align: left"> Passionate Investors </td>
            <td style="text-align: center"> 3% </td>
        </tr>
        <tr>
            <td style="text-align: left"> True Heroes of the Great Web </td>
            <td style="text-align: center"> 5% </td>
        </tr>
    </tbody>
</table>

### Distribution between Grades

An amount of distributed CYB tokens should be equal for each grade within an audience.  
Also amount of addresses should be divided into grades for each audience as

<table style="text-align: left">
    <thead style="text-align: center">
        <tr>
            <th> Grade </th>
            <th> Share of Address Amount </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align: center"> 1 </td>
            <td style="text-align: center"> 89% </td>
        </tr>
        <tr>
            <td style="text-align: center"> 2 </td>
            <td style="text-align: center"> 10% </td>
        </tr>
        <tr>
            <td style="text-align: center"> 3 </td>
            <td style="text-align: center"> 1% </td>
        </tr>
    </tbody>
</table>

### Prize to be the First 

There will be incentive **20x** for those who claim first reducing to **5x** who came last.  
This condition does not apply to the audience of the Manual Set Addresses.  
So only **~1/10** accounts will be actually claim a gift.

### Excluding Fiat Brains 

Addresses based on the fiat system will not be included, 
namely those that satisfy these two conditions:
- Stablecoin balance more than sum of ETH and [selected ERC20 tokens](passionate_investors_and_cryptopunks__erc20_analysis.ipynb) balances
- Stablecoin balance more than 0.1 ETH 

## Audiences

### Average Citizens. ETH Analysis

[ETH Analysis](average_citizens__eth_analysis.ipynb)

### Cyberpunks. ERC20 and ERC721 Analysis

[ERC20 Analysis](passionate_investors_and_cryptopunks__erc20_analysis.ipynb)  
[ERC721 Analysis](masters_and_cryptopunks__erc721_analysis.ipynb)  
[Urbit Analysis](cryptopunks_urbit_analysis.ipynb)

### Extraordinary Hackers. Gas Analysis

To search for **Extraordinary Hackers** who have created the Ethereum ecosystem, I will be aggregate the used gas by creators of contracts and factories.  
To do this, I want to calculate an amount of gas used for contracts calls.  
[Gas Analysis](extraordinary_hackers_and_masters__gas_analysis.ipynb)

### Key Opinion Leaders. Top 100 ERC20 Holders by Tokens

[Top 100 ERC20 Holders](leaders__top_erc20_holders.ipynb)

### Masters of the Great Web. Gas and ERC721 Analysis

[Gas Analysis](extraordinary_hackers_and_masters__gas_analysis.ipynb)  
[ERC721 Analysis](masters_and_cryptopunks__erc721_analysis.ipynb)

### Passionate Investors. ERC20 Analysis

[ERC20 Analysis](passionate_investors_and_cryptopunks__erc20_analysis.ipynb)

### True Heroes of the Great Web. Genesis and ETH2 Stakers

[Genesis and ETH2 Stakers](heroes__genesis_and_eth2_stakers.ipynb)

### Manual Assigned Addresses

[Setting Addresses](manual_set_addresses.ipynb)

### Astronauts. ATOM Analysis

[ATOM Analysis](astronauts__atom_analysis.ipynb)

## Final Distribution

[Jupyter Notebook](final_distribution.ipynb)  
[Dashboard](https://datastudio.google.com/u/0/reporting/53e1c28b-9f10-497c-9b5b-9f2a4749450b)
