def flatten_structure(data):
    flattened = []

    def walk(value, path):
        if isinstance(value, dict):
            for key, val in value.items():
                walk(val, path + [key])
        elif isinstance(value, list):
            for idx, val in enumerate(value, 1):  # Enumerate lists starting from 1
                walk(val, path + [idx])
        else:
            flattened.append((path, value))
    walk(data, [])

    return flattened

# Test case
test_dict = {
    'level1': {
        'first': ["a", "b", {"deep1": "val1", "deep2": ["g", "h", "i"]}],
        'second': ["c", "d"],
        'third': {
            'nested1': ["e", "f"],
            'nested2': {
                'subnested1': {"key1": 1, "key2": [10, 20]},
                'subnested2': ("tuple1", "tuple2")
            }
        }
    },
    'level2': {
        'fourth': {
            'deepnested': {
                'deepest': [{"keyA": "alpha"}, {"keyB": "beta"}]
            }
        },
        'fifth': {"obj": ("item1", "item2", {"keyC": "gamma"})}
    },
    'level3': set([frozenset([1, 2]), frozenset([3, 4])]),
    'sixth': bytes([10, 20, 30]),
}


flattened_result = flatten_structure(test_dict)
for item in flattened_result:
    print(item)



def dispatcher(obj, func):
    if isinstance(obj, dict):
        return {key: func(value, key) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [func(item) for item in obj]
