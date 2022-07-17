import requests
import ast

from config import GRAPHQL_API, HEADERS


def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post(GRAPHQL_API, json={'query': query}, headers=HEADERS)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def get_data(address) -> list:
    query = '''{
                  cyber_gift_proofs(where: {address: {_eq: "%s"}}) {
                        address
                        amount
                        details
                  }
                }''' % address
    result = run_query(query)
    return result['data']['cyber_gift_proofs']


def format_for_aggregate(address: str) -> ():
    data = get_data(address)
    audience = []
    grade = []
    segment = []
    try:
        gift = int(data[0]['amount'] / 1_000_000)
        details = ast.literal_eval(data[0]['details'])
        for x in details:
            audience.append(x['audience'])
            grade.append(x['grade'])
            segment.append(x['segment'])
    except IndexError:
        gift = 0
    return gift, audience, grade, segment


def format_for_full_data(address: str) -> list:
    data = get_data(address)
    details = ast.literal_eval(data[0]['details'])
    result = []
    for x in details:
        result.append({
                            "denom": "Mboot",
                            "address": data[0]['address'],
                            "gift": x['gift'],
                            "claimed": False,
                            "claimed_amount": "0",
                            "unclaimed_amount": x['gift'],
                            "audience": x['audience'],
                            "grade": x['grade'],
                            "segment": x['segment']
        })
    return result


def get_incentive_coef() -> float:
    # TODO add query from Gift contract
    return 12
