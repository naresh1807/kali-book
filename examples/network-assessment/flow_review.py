"""Offline TCP reachability evidence review. No network requests or firewall changes."""
import ipaddress
import json
from pathlib import Path

REQUIRED = {"name", "source_zone", "destination", "protocol", "port", "expected", "observed"}

def evaluate(row):
    if not isinstance(row, dict) or set(row) != REQUIRED:
        raise ValueError("Use the exact documented row schema")
    if not all(isinstance(row[k], str) and row[k] for k in REQUIRED - {"port"}):
        raise ValueError("Text fields must be nonempty strings")
    address = ipaddress.ip_address(row["destination"])
    if address not in ipaddress.ip_network("192.0.2.0/24"):
        raise ValueError("This teaching fixture accepts only documentation addresses")
    if row["protocol"] != "tcp" or type(row["port"]) is not int or not 1 <= row["port"] <= 65535:
        raise ValueError("This model requires TCP and a valid integer port")
    expected, observed = row["expected"], row["observed"]
    if expected not in ("allow", "deny") or observed not in ("reachable", "policy_blocked", "timeout", "closed"):
        raise ValueError("Unknown expectation or evidence category")
    if observed == "timeout" or (expected == "deny" and observed == "closed"):
        return "inconclusive"
    if expected == "allow":
        return "pass" if observed == "reachable" else "fail"
    return "pass" if observed == "policy_blocked" else "fail"

def review(rows):
    if not isinstance(rows, list):
        raise ValueError("Expected a list of flow records")
    return [{"name": row["name"], "result": evaluate(row)} for row in rows]

if __name__ == "__main__":
    rows = json.loads(Path(__file__).with_name("flows.json").read_text(encoding="utf-8"))
    results = review(rows)
    print(json.dumps({"synthetic": True, "results": results}, indent=2))
    # Demonstration succeeds only when its deliberate failures and unknowns are recognized.
    raise SystemExit(0 if [r["result"] for r in results] == ["pass", "fail", "pass", "inconclusive", "inconclusive", "fail"] else 1)
