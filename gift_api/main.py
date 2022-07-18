from flask import Flask, jsonify, render_template
from cyberpy._wallet import address_to_address

from config import API_HOST, API_PORT
from graphql import format_for_aggregate, format_for_full_data, get_incentive_coef

app = Flask(__name__)


@app.route('/cyber_gift_aggregate/<address>', methods=['GET'])
def cyber_gift_aggregate(address: str):
    address = address.lower()
    total_amount, audience, grade, segment = format_for_aggregate(address)
    if total_amount == 0:
        return render_template('403.html'), 403
    try:
        return jsonify(
            {
                "denom": "Mboot",
                "address": address,
                "total_amount": total_amount,
                "claimed": False,
                "claimed_amount": "0",
                "unclaimed_amount": total_amount,
                "audience": audience,
                "grade": grade,
                "segment": segment
            }
        )
    except Exception:
        return render_template('403.html'), 403


@app.route('/cyber_gift_aggregate_by_pubkey/<address>', methods=['GET'])
def cyber_gift_aggregate_by_pubkey(address: str):
    address = address.lower()
    try:
        if len(address) > 42 and address[: 4] in ('osmo', 'cosm', 'bost'):
            address_cosmos = address_to_address(address, 'cosmos')
            address_osmosis = address_to_address(address, 'osmo')
            total_amount_cosmos, _, _, _ = format_for_aggregate(address_cosmos)
            total_amount_osmosis, _, _, _ = format_for_aggregate(address_osmosis)
            total_amount = total_amount_cosmos + total_amount_osmosis
        else:
            total_amount, _, _, _ = format_for_aggregate(address)
        if total_amount == 0:
            return render_template('403.html'), 403
        total_amount = int(int(total_amount) * 1_000_000 * get_incentive_coef())
        return jsonify(
            {
                "denom": "boot",
                "address": address,
                "total_amount": total_amount
            }
        )
    except Exception as e:
        print(f'Error: {e}')
        return render_template('403.html'), 403


@app.route('/cyber_gift_full_data/<address>', methods=['GET'])
def cyber_gift_full_data(address: str):
    address = address.lower()
    result = format_for_full_data(address)
    if not result:
        return render_template('403.html'), 403
    try:
        return jsonify(
            result
        )
    except Exception:
        return render_template('403.html'), 403


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)
