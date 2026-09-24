import json
record = json.loads('{"status":200,"path":"/"}')
if not isinstance(record, dict):
    raise ValueError("Expected an object")
if type(record.get("status")) is not int:
    raise ValueError("Expected integer status")
print(json.dumps(record, sort_keys=True))
