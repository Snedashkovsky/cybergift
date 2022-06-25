from flask import Flask, jsonify, render_template

from config import API_HOST, API_PORT
from graphql import format_for_aggregate, format_for_full_data


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
