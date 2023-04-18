# conftest.py

def pytest_collection_modifyitems(items):
    for item in items:
        item._nodeid = item._request.node.callspec.params['teszt'][0] + '::' + item._request.node.callspec.params['teszt'][1]
