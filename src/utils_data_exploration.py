from pprint import pprint


def json_explore(explorable_json):
    for key in explorable_json.keys():
        try:
            print(f'\n{key} keys:  {list(explorable_json[key].keys()) if explorable_json[key] is not None else 0}')
        except KeyError:
            print(f'\n{key} no keys, KeyError')
        except AttributeError:
            if isinstance(explorable_json[key], str):
                print(f"\n{key}: {explorable_json[key]}")
            elif isinstance(explorable_json[key], list) and len(explorable_json[key]) > 0:
                print(f"\n{key} the first item:\n")
                pprint(explorable_json[key][0])
            elif isinstance(explorable_json[key], list):
                print(f"\n{key}: {explorable_json[key]}")
            else:
                print(f"\n{key} no keys, 'str' object has no attribute 'keys'")
