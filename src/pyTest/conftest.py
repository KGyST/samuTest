def pytest_collection_modifyitems(items):
    for item in items:
        item._nodeid = f"{item._request.node.callspec.params['p_testCase']['args'][0]}::{item._request.node.callspec.params['p_testCase']['args'][0]}"

