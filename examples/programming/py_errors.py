import json
try:
    json.loads("invalid JSON")
except json.JSONDecodeError as error:
    print("Invalid JSON at character", error.pos)
