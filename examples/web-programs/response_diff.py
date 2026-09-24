import hashlib, json, sys
from pathlib import Path

def load(path):
    with Path(path).open("rb") as f: data = f.read(1048577)
    if len(data)>1048576: raise ValueError("File too large")
    row=json.loads(data.decode("utf-8"))
    if not isinstance(row,dict) or type(row.get("status")) is not int or not 100<=row["status"]<=599 or not isinstance(row.get("body"),str):
        raise ValueError("Expected status integer 100..599 and body string")
    return row

def compare(a,b):
    return {"same_status":a["status"]==b["status"], "same_body":a["body"]==b["body"], "body_bytes":[len(x["body"].encode("utf-8")) for x in (a,b)], "sha256":[hashlib.sha256(x["body"].encode("utf-8")).hexdigest() for x in (a,b)], "note":"Different responses do not prove broken authorization. Verify identity, expected permissions and returned data."}

if __name__=="__main__":
    if len(sys.argv)!=3: sys.exit("Usage: python3 response_diff.py baseline.json comparison.json")
    try: print(json.dumps(compare(load(sys.argv[1]),load(sys.argv[2])),sort_keys=True))
    except (ValueError,OSError): sys.exit("Cannot compare: invalid or unreadable input")
