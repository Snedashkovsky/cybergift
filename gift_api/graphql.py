import requests
from config import GRAPHQL_API, HEADERS


def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post(GRAPHQL_API, json={'query': query}, headers=HEADERS)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def get_data(address) -> list:
    query = '''{
                  cyber_gift(where: {address: {_eq: "%s"}}) {
                        address
                        audience
                        gift
                        grade
                        segment
                  }
                }''' % address
    result = run_query(query)
    return result['data']['cyber_gift']


def format_for_aggregate(address: str) -> ():
    data = get_data(address)
    gift = 0.0
    audience = []
    grade = []
    segment = []
    for x in data:
        gift += float(x['gift'])
        audience.append(x['audience'])
        grade.append(x['grade'])
        segment.append(x['segment'])
    return gift, audience, grade, segment


def format_for_full_data(address: str) -> list:
    data = get_data(address)
    result = []
    for x in data:
        result.append({
                            "denom": "Mboot",
                            "address": x['address'],
                            "gift": x['gift'],
                            "claimed": False,
                            "claimed_amount": "0",
                            "unclaimed_amount": x['gift'],
                            "audience": x['audience'],
                            "grade": x['grade'],
                            "segment": x['segment']
        })
    return result