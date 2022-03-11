import pandas as pd
import json
from math import floor


def get_coin_balance(balance: list, coin: str = 'uatom', decimals: int = 6) -> float:
    for _balance_item in balance:
        if _balance_item['denom'] == coin:
            return float(_balance_item['amount']) / 10 ** decimals
    return 0.0


def get_osmo_prices(genesis_snapshot: json) -> [dict, pd.DataFrame]:
    # Get pools data and all denoms from snapshot
    _pools = genesis_snapshot["app_state"]['gamm']['pools']
    _pool_denoms = [pool['totalShares']['denom'] for pool in _pools]
    _token_denoms = [token['token']['denom'] for pool in _pools for token in pool['poolAssets']]
    _denoms = set(_token_denoms + _pool_denoms)

    _price_df = pd.DataFrame(columns=_denoms, index=_denoms)
    _osmo_price_dict = {}

    for _pool in _pools:
        _pool_denom = _pool['totalShares']['denom']
        _pool_supply = int(_pool['totalShares']['amount'])
        _pool_assets = _pool['poolAssets']
        _item_denoms = [token['token']['denom'] for token in _pool_assets]
        _item_amounts = [int(token['token']['amount']) for token in _pool_assets]

        for _denom1, _amount1 in zip(_item_denoms, _item_amounts):
            _price_df.loc[_pool_denom, _denom1] = _amount1 / _pool_supply * 2
            _price_df.loc[_denom1, _pool_denom] = _pool_supply / _amount1 / 2
            for _denom2, _amount2 in zip(_item_denoms, _item_amounts):
                _price_df.loc[_denom2, _denom1] = _amount1 / _amount2
                _price_df.loc[_denom1, _denom2] = _amount2 / _amount1
        try:
            osmo_index = _item_denoms.index('uosmo')
            if _pool_denom not in _osmo_price_dict.keys():
                _osmo_price_dict[_pool_denom] = _price_df.loc[_pool_denom, _item_denoms[osmo_index]]
            for _denom in _item_denoms:
                if _denom not in _osmo_price_dict.keys():
                    _osmo_price_dict[_denom] = _price_df.loc[_denom, _item_denoms[osmo_index]]

        except ValueError:
            _denoms_with_price = [denom for denom in _item_denoms if denom in _osmo_price_dict.keys()]
            try:
                _denom_with_price_index = _item_denoms.index(_denoms_with_price[0])
                if _pool_denom not in _osmo_price_dict.keys():
                    _osmo_price_dict[_pool_denom] = _price_df.loc[_pool_denom, _item_denoms[_denom_with_price_index]] * \
                                                    _osmo_price_dict[_item_denoms[_denom_with_price_index]]
                for _denom in _item_denoms:
                    if _denom not in _osmo_price_dict.keys():
                        _osmo_price_dict[_denom] = _price_df.loc[_denom, _item_denoms[_denom_with_price_index]] * \
                                                   _osmo_price_dict[_item_denoms[_denom_with_price_index]]
            except (ValueError, KeyError):
                pass
    return _osmo_price_dict, _price_df


def get_liquidity_from_balance(balances: list, price_dict: dict, decimals: int = 6) -> float:
    _amount = 0.0
    for _balance in balances:
        if _balance['denom'][:10] == 'gamm/pool/':
            _amount += int(_balance['amount']) * price_dict[_balance['denom']]
    return _amount / 10 ** decimals


def get_liquidity(genesis_snapshot: json) -> pd.DataFrame:
    _osmo_price_dict, _ = get_osmo_prices(genesis_snapshot=genesis_snapshot)

    # Get balance of unstaked pools coins
    _available_balances_df = pd.DataFrame(genesis_snapshot["app_state"]['bank']['balances'])
    _available_balances_df['unstaked_liquidity'] = _available_balances_df['coins'].map(
        lambda x: get_liquidity_from_balance(balances=x, price_dict=_osmo_price_dict))
    _available_balances_df = _available_balances_df.groupby('address')['unstaked_liquidity'].agg(sum).reset_index()

    # Get balance of staked pools coins
    _lockup_df = pd.DataFrame(genesis_snapshot["app_state"]['lockup']['locks'])
    _lockup_df['staked_liquidity'] = _lockup_df['coins'].map(
        lambda x: get_liquidity_from_balance(balances=x, price_dict=_osmo_price_dict))
    _lockup_df.rename(columns={'owner': 'address'}, inplace=True)
    _lockup_df = _lockup_df.groupby('address')['staked_liquidity'].agg(sum).reset_index()

    _liquidity_df = _available_balances_df[['address', 'unstaked_liquidity']].merge(
        _lockup_df[['address', 'staked_liquidity']],
        how='outer',
        on='address').fillna(0.0)
    _liquidity_df['liquidity'] = _liquidity_df['unstaked_liquidity'] + _liquidity_df['staked_liquidity']

    return _liquidity_df[_liquidity_df.liquidity > 0]


def get_available_balances(genesis_snapshot: json, coin: str) -> pd.DataFrame:
    _available_balances_df = pd.DataFrame(genesis_snapshot["app_state"]['bank']['balances'])
    _available_balances_df.loc[:, 'available_coin'] = _available_balances_df.coins.map(
        lambda x: get_coin_balance(balance=x, coin=coin))
    _available_balances_df = _available_balances_df[_available_balances_df.available_coin != 0]
    _available_balances_df['address'] = _available_balances_df['address'].map(lambda x: x.lower())
    return _available_balances_df.groupby('address')['available_coin'].agg(sum).reset_index()


def get_delegated_balances(genesis_snapshot: json, decimals: int = 6) -> pd.DataFrame:
    _delegated_balances_df = \
        pd.DataFrame(genesis_snapshot["app_state"]['staking']['delegations'])[['delegator_address', 'shares']] \
            .rename(columns={'delegator_address': 'address'})
    _delegated_balances_df['address'] = _delegated_balances_df['address'].map(lambda x: x.lower())
    _delegated_balances_df.loc[:, 'delegated_coin'] = _delegated_balances_df['shares'].map(
        lambda x: float(x) / 10 ** decimals)
    return _delegated_balances_df.groupby('address')['delegated_coin'].agg(sum).reset_index()


def get_unbonding_delegations(genesis_snapshot: json, decimals: int = 6) -> pd.DataFrame:
    return pd.DataFrame(
        [[unbonding_delegation['delegator_address'].lower(),
          sum([float(entry['balance']) for entry in unbonding_delegation['entries']]) / 10 ** decimals]
         for unbonding_delegation in genesis_snapshot["app_state"]['staking']['unbonding_delegations']],
        columns=['address', 'unbonding_coin']).groupby('address')['unbonding_coin'].agg(sum).reset_index()


def get_balances(snapshot_url: str, coin: str) -> pd.DataFrame:
    with open(snapshot_url) as _f:
        _genesis_snapshot = json.load(_f)

    # Get Available, Delegated balances and Unbonding delegations
    _available_balances_df = get_available_balances(genesis_snapshot=_genesis_snapshot, coin=coin)
    _delegated_balances_df = get_delegated_balances(genesis_snapshot=_genesis_snapshot)
    _unbonding_delegations_df = get_unbonding_delegations(genesis_snapshot=_genesis_snapshot)

    # Get module and pool addresses
    _module_addresses_list = \
        [item['base_account']['address'] for item in _genesis_snapshot['app_state']['auth']['accounts']
         if item['@type'] in ('/cosmos.auth.v1beta1.ModuleAccount', '/osmosis.gamm.v1beta1.Pool')]

    # Merge Available and Delegated balances
    _balances_df = \
        _available_balances_df[['address', 'available_coin']].merge(
            _delegated_balances_df[['address', 'delegated_coin']],
            how='outer',
            on='address'
        ).merge(
            _unbonding_delegations_df[['address', 'unbonding_coin']],
            how='outer',
            on='address'
        ).fillna(0)

    # Add Osmosis liquidity
    if coin == 'uosmo':
        _liquidity_df = get_liquidity(genesis_snapshot=_genesis_snapshot)
        _balances_df = \
            _balances_df.merge(
                _liquidity_df,
                how='outer',
                on='address'
            ).fillna(0)
        _balances_df.loc[:, 'balance_coin'] = _balances_df[
            ['available_coin', 'delegated_coin', 'unbonding_coin', 'liquidity']].sum(axis=1)
    else:
        _balances_df.loc[:, 'balance_coin'] = _balances_df[['available_coin', 'delegated_coin', 'unbonding_coin']].sum(
            axis=1)

    # Round balance and remove module, pool addresses
    _balances_df.loc[:, 'balance_coin_rounded'] = \
        _balances_df.balance_coin.map(lambda x: floor(x) + 0.5 if x > 1 else 0.5)
    return _balances_df[~_balances_df['address'].isin(_module_addresses_list)]
