def pytest_generate_tests(metafunc):
    params = generate_cases()
    metafunc.parametrize('arg', params)

def generate_cases():
    return [
        [1, 1],
        [2, 2],
        [3, 3],
        ]
