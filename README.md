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
            <td style="text-align: left"> Manual Assigned Addresses </td>
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

![](img/incentive_chart.png)
### Excluding Fiat Brains 

Addresses based on the fiat system will not be included, 
namely those that satisfy these two conditions:
- Stablecoin balance more than sum of ETH and [selected ERC20 tokens](erc20__investors_and_cyberpunks.ipynb) balances
- Stablecoin balance more than 0.1 ETH 

## Audience Rules

<table style="text-align: left">
    <thead style="text-align: center">
        <tr>
            <th rowspan=2>Audience</th>
            <th rowspan=2>Rule</th>
            <th colspan=3>Grade</th>
            <th rowspan=2>Calculations</th>
        </tr>
        <tr>
            <th>1</th>
            <th>2</th>
            <th>3</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align: left"> Astronauts </td>
            <td style="text-align: left"> ATOM Balance </td>
            <td style="text-align: center"> > 0 ATOM </td>
            <td style="text-align: center"> > 178 ATOM </td>
            <td style="text-align: center"> > 6,191 ATOM </td>
            <td style="text-align: center"> <a href="atom__astronauts.ipynb">ATOM Analysis</a> </td>
        </tr>
        <tr>
            <td rowspan=2 style="text-align: left"> Average Citizens </td>
            <td style="text-align: left"> ETH balance > 0.01 ETH and Amount of outgoing tx</td>
            <td style="text-align: center"> > 3 tx </td>
            <td style="text-align: center"> > 60 tx </td>
            <td style="text-align: center"> > 657 tx </td>
            <td rowspan=2 style="text-align: center"> <a href="eth_and_tx__citizens.ipynb">ETH Analysis</a> </td>
        </tr>
        <tr>
            <td style="text-align: left"> ETH balance</td>
            <td style="text-align: center"> > 1 ETH</td>
            <td style="text-align: center"> > 32 ETH</td>
            <td style="text-align: center"> > 551 ETH</td>
        </tr>
        <tr>
            <td rowspan=3 style="text-align: left"> Cyberpunks </td>
            <td style="text-align: left"> Owners of the Selected ERC20 tokens </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> FOAM or GOLD </td>
            <td style="text-align: center"> <a href="erc20__investors_and_cyberpunks.ipynb">ERC20 Analysis</a> </td>
        </tr>
        <tr>
            <td style="text-align: left"> Owners of the Selected ERC721 tokens </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> Unicorns, DRAGON or Cryptopunks </td>
            <td style="text-align: center"> <a href="erc721__masters_and_cyberpunks.ipynb">ERC721 Analysis</a> </td>
        </tr>
        <tr>
            <td style="text-align: left"> Urbit Owners </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> here </td>
            <td style="text-align: center"> <a href="urbit__cyberpunks.ipynb">Urbit Analysis</a> </td>
        </tr>
        <tr>
            <td rowspan=2 style="text-align: left"> Extraordinary Hackers </td>
            <td> Fee spending to created contracts<sup>1</sup> by contract creators<sup>2</sup> </td>
            <td style="text-align: center"> > 0 ETH </td>
            <td style="text-align: center"> > 4 ETH </td>
            <td style="text-align: center"> > 233 ETH </td>
            <td rowspan=2 style="text-align: center"> <a href="gas__hackers_and_masters.ipynb">Gas Analysis</a> </td>
        </tr>
        <tr>
            <td style="text-align: left"> Fee spending to created contracts<sup>1</sup> by factory creators<sup>3</sup> </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> > 0 ETH </td>
            <td style="text-align: center"> > 10 ETH </td>
        </tr>
        <tr>
            <td style="text-align: left"> Key Opinion Leaders </td>
            <td style="text-align: left"> Top 100 ERC20 Holders by Tokens </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> only here </td>
            <td style="text-align: center"> <a href="erc20__leaders.ipynb">Top 100 ERC20 Holders</a> </td>
        </tr>
        <tr>
            <td style="text-align: left"> Manual Assigned Addresses </td>
            <td style="text-align: left"> - </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> only here </td>
            <td style="text-align: center"> <a href="manual_assigned_addresses.ipynb">Assigning Addresses</a> </td>
        </tr>
        <tr>
            <td rowspan=3 style="text-align: left"> Masters of the Great Web </td>
            <td style="text-align: left"> Amount of ERC721 tokens </td>
            <td style="text-align: center"> > 0 NFT </td>
            <td style="text-align: center"> > 7 NFT </td>
            <td style="text-align: center"> > 186 NFT </td>
            <td rowspan=2 style="text-align: center"> <a href="erc721__masters_and_cyberpunks.ipynb">ERC721 Analysis</a> </td>
        </tr>
        <tr>
            <td style="text-align: left"> Owners of the Selected ERC721 tokens </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> ENS </td>
            <td style="text-align: center" style="text-align: center"> Gitcoin Kudos or LAND </td>
        </tr>
        <tr>
            <td style="text-align: left"> Fee spending to contracts<sup>4</sup>, by contract creators, ETH </td>
            <td style="text-align: center"> > 0 ETH </td>
            <td style="text-align: center"> > 0.005 ETH </td>
            <td style="text-align: center"> > 0.755 ETH </td>
            <td style="text-align: center"> <a href="gas__hackers_and_masters.ipynb">Gas Analysis</a> </td>
        </tr>
        <tr>
            <td style="text-align: left"> Passionate Investors </td>
            <td style="text-align: left"> Number of tokens >= 2 and ERC20 balance </td>
            <td style="text-align: center"> > 0.01 ETH </td>
            <td style="text-align: center"> > 6 ETH </td>
            <td style="text-align: center"> > 88 ETH </td>
            <td style="text-align: center"> <a href="erc20__investors_and_cyberpunks.ipynb">ERC20 Analysis</a> </td>
        </tr>
        <tr>
            <td rowspan=2 style="text-align: left"> True Heroes of the Great Web </td>
            <td style="text-align: left"> Genesis </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> only here </td>
            <td rowspan=2 style="text-align: center"> <a href="genesis_and_eth2__heroes.ipynb">Genesis and ETH2 Stakers</a> </td>
        </tr>
        <tr>
            <td style="text-align: left"> ETH 2.0 Stakers </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> - </td>
            <td style="text-align: center"> only here </td>
        </tr>
        <tr>
            <td colspan=5 style="text-align: left"> Final Distribution </td>
            <td style="text-align: center"> <a href="final_distribution.ipynb">Final Distribution</a></td>
        </tr>
    </tbody>
</table>
<i>
<sup>1</sup>  excluding fee from a contract creator address<br>
<sup>2</sup>  excluding contracts created by factories<br>
<sup>3</sup>  excluding factories that only created contracts when called from the creator of that factory<br>
<sup>4</sup> including contracts created by factories only<br>
</i>


## Final Distribution

[Final Distribution Table](https://console.cloud.google.com/bigquery?project=cosmic-keep-223223&p=cosmic-keep-223223&d=final&t=final_distribution&page=table&ws=!1m5!1m4!4m3!1scosmic-keep-223223!2sfinal!3sfinal_distribution)  
**Check your address in the [Dashboard](https://datastudio.google.com/u/0/reporting/53e1c28b-9f10-497c-9b5b-9f2a4749450b)**
