_list = [1, 2, 3, 4, 5,]
_result = []

for item in _list:
    _result = [item, *_result]

_result = _list[::-1]

_result = {}

for k, v in zip(range(1, len(_list)), _list):
    _result[k] = v

print(_result)
