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
    'first': ["a", "b"],
    'second': ["c", "d"],
    'third': {'nested': ["e", "f"]}  # Nested structure
}

flattened_result = flatten_structure(test_dict)
for item in flattened_result:
    print(item)
